
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core import database
from app.main import app


@pytest.fixture
def api_client(tmp_path, monkeypatch):
    """Create a test client using an isolated temporary database."""
    test_db = tmp_path / "api_test.db"
    monkeypatch.setattr(database.settings, "database_path", test_db)

    with TestClient(app) as client:
        yield client


def test_create_memory_returns_201(api_client):
    response = api_client.post(
        "/api/v1/memories",
        json={
            "content": "Learned gradient descent",
            "memory_type": "learning",
        },
    )

    assert response.status_code == 201

    memory = response.json()
    assert memory["id"]
    assert memory["content"] == "Learned gradient descent"
    assert memory["memory_type"] == "learning"
    assert memory["created_at"]
    assert memory["updated_at"] == memory["created_at"]


def test_get_memory_by_id(api_client):
    created = api_client.post(
        "/api/v1/memories",
        json={
            "content": "Built a semantic search project",
            "memory_type": "project",
        },
    )
    assert created.status_code == 201

    memory_id = created.json()["id"]

    response = api_client.get(f"/api/v1/memories/{memory_id}")

    assert response.status_code == 200
    assert response.json()["id"] == memory_id
    assert response.json()["content"] == "Built a semantic search project"


def test_unknown_memory_returns_404(api_client):
    response = api_client.get(
        "/api/v1/memories/00000000-0000-4000-8000-000000000000"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Memory not found"


def test_list_memories_returns_newest_first(api_client):
    first_response = api_client.post(
        "/api/v1/memories",
        json={
            "content": "First memory",
            "memory_type": "learning",
        },
    )
    assert first_response.status_code == 201
    first = first_response.json()

    second_response = api_client.post(
        "/api/v1/memories",
        json={
            "content": "Second memory",
            "memory_type": "project",
        },
    )
    assert second_response.status_code == 201
    second = second_response.json()

    response = api_client.get("/api/v1/memories")

    assert response.status_code == 200
    result = response.json()

    assert result["count"] == 2
    assert len(result["memories"]) == 2
    assert {item["id"] for item in result["memories"]} == {
        first["id"],
        second["id"],
    }

    # Match the service's ordering: created_at DESC, then id DESC.
    expected = sorted(
        [first, second],
        key=lambda item: (item["created_at"], item["id"]),
        reverse=True,
    )

    assert [item["id"] for item in result["memories"]] == [
        item["id"] for item in expected
    ]


@pytest.mark.parametrize(
    "payload",
    [
        {"content": "", "memory_type": "learning"},
        {"content": "   ", "memory_type": "learning"},
        {"content": "Valid content", "memory_type": "invalid"},
        {"content": "x" * 10001, "memory_type": "learning"},
        {"content": "Missing type"},
        {"memory_type": "learning"},
    ],
)
def test_invalid_memory_payload_returns_422(api_client, payload):
    response = api_client.post(
        "/api/v1/memories",
        json=payload,
    )

    assert response.status_code == 422


def test_memory_endpoints_appear_in_openapi(api_client):
    response = api_client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]

    assert "/api/v1/memories" in paths
    assert "post" in paths["/api/v1/memories"]
    assert "get" in paths["/api/v1/memories"]
    assert "/api/v1/memories/{memory_id}" in paths
    assert "get" in paths["/api/v1/memories/{memory_id}"]
