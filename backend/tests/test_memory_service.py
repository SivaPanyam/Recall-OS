
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core import database
from app.services import memory_service


@pytest.fixture
def temporary_database(tmp_path, monkeypatch):
    db_path = tmp_path / "service_test.db"
    monkeypatch.setattr(database.settings, "database_path", db_path)
    database.initialize_database()
    return db_path


def test_create_memory_returns_saved_record(temporary_database):
    memory = memory_service.create_memory(
        "Learned gradient descent",
        "learning",
    )

    assert memory["id"]
    assert memory["content"] == "Learned gradient descent"
    assert memory["memory_type"] == "learning"
    assert memory["created_at"]
    assert memory["updated_at"] == memory["created_at"]

    saved = memory_service.get_memory(memory["id"])
    assert saved == memory


def test_get_memory_returns_none_for_unknown_id(temporary_database):
    result = memory_service.get_memory(
        "00000000-0000-4000-8000-000000000000"
    )

    assert result is None


def test_list_memories_returns_newest_first(temporary_database):
    older = memory_service.create_memory("Older memory", "learning")
    newer = memory_service.create_memory("Newer memory", "project")

    memories = memory_service.list_memories()

    assert len(memories) == 2
    assert memories[0]["id"] == newer["id"]
    assert memories[1]["id"] == older["id"]


def test_create_memory_rejects_whitespace_content(temporary_database):
    with pytest.raises(Exception):
        memory_service.create_memory("   ", "learning")


def test_create_memory_rejects_invalid_memory_type(temporary_database):
    with pytest.raises(Exception):
        memory_service.create_memory("Valid content", "invalid")
