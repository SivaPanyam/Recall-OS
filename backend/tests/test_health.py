
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import HealthResponse, RootResponse

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to OES",
        "status": "running",
    }
    assert RootResponse.model_validate(response.json())


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "oes-backend",
        "version": "0.1.0",
    }
    assert HealthResponse.model_validate(response.json())


def test_openapi_documents_response_schemas():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schemas = response.json()["components"]["schemas"]

    assert "RootResponse" in schemas
    assert "HealthResponse" in schemas

    root_schema = schemas["RootResponse"]
    assert set(root_schema["required"]) == {"message", "status"}

    health_schema = schemas["HealthResponse"]
    assert set(health_schema["required"]) == {
        "status",
        "service",
        "version",
    }

def test_health_endpoint_uses_configured_version(monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "app_version", "9.9.9")

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["version"] == "9.9.9"


def test_unknown_endpoint_returns_404():
    response = client.get("/api/v1/nonexistent")

    assert response.status_code == 404
