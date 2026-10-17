
import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core import database


@pytest.fixture
def temporary_database(tmp_path, monkeypatch):
    db_path = tmp_path / "oes_test.db"
    monkeypatch.setattr(database.settings, "database_path", db_path)
    return db_path


def test_initialize_database_creates_memories_table(temporary_database):
    database.initialize_database()

    with database.get_connection() as connection:
        result = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'memories'
            """
        ).fetchone()

    assert result is not None
    assert result["name"] == "memories"


def test_initialize_database_is_idempotent(temporary_database):
    database.initialize_database()
    database.initialize_database()

    with database.get_connection() as connection:
        tables = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM sqlite_master
            WHERE type = 'table' AND name = 'memories'
            """
        ).fetchone()

    assert tables["count"] == 1


def test_database_rejects_empty_content(temporary_database):
    database.initialize_database()

    with pytest.raises(sqlite3.IntegrityError):
        with database.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO memories
                    (id, content, memory_type, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    "memory-1",
                    "   ",
                    "learning",
                    "2026-10-17T00:00:00+00:00",
                    "2026-10-17T00:00:00+00:00",
                ),
            )


def test_database_rejects_invalid_memory_type(temporary_database):
    database.initialize_database()

    with pytest.raises(sqlite3.IntegrityError):
        with database.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO memories
                    (id, content, memory_type, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    "memory-2",
                    "Test memory",
                    "invalid",
                    "2026-10-17T00:00:00+00:00",
                    "2026-10-17T00:00:00+00:00",
                ),
            )


def test_memory_persists_after_reopening_connection(temporary_database):
    database.initialize_database()

    with database.get_connection() as connection:
        connection.execute(
            """
            INSERT INTO memories
                (id, content, memory_type, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "memory-3",
                "SQLite persistence test",
                "learning",
                "2026-10-17T00:00:00+00:00",
                "2026-10-17T00:00:00+00:00",
            ),
        )

    with database.get_connection() as connection:
        result = connection.execute(
            "SELECT content FROM memories WHERE id = ?",
            ("memory-3",),
        ).fetchone()

    assert result is not None
    assert result["content"] == "SQLite persistence test"


def test_database_rejects_content_over_10000_characters(
    temporary_database,
):
    database.initialize_database()

    with pytest.raises(sqlite3.IntegrityError):
        with database.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO memories
                    (id, content, memory_type, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    "memory-4",
                    "x" * 10001,
                    "learning",
                    "2026-10-17T00:00:00+00:00",
                    "2026-10-17T00:00:00+00:00",
                ),
            )
