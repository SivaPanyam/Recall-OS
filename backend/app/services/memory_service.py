
from datetime import datetime, timezone
import uuid

from app.core import database


def _utc_now() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def create_memory(content: str, memory_type: str) -> dict:
    """Create a memory and return its stored representation."""
    now = _utc_now()

    memory = {
        "id": str(uuid.uuid4()),
        "content": content,
        "memory_type": memory_type,
        "created_at": now,
        "updated_at": now,
    }

    connection = database.get_connection()
    try:
        with connection:
            connection.execute(
                """
                INSERT INTO memories (
                    id, content, memory_type, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    memory["id"],
                    memory["content"],
                    memory["memory_type"],
                    memory["created_at"],
                    memory["updated_at"],
                ),
            )
    finally:
        connection.close()

    return memory


def get_memory(memory_id: str) -> dict | None:
    """Retrieve a memory by ID, or return None if it does not exist."""
    connection = database.get_connection()
    try:
        row = connection.execute(
            """
            SELECT id, content, memory_type, created_at, updated_at
            FROM memories
            WHERE id = ?
            """,
            (memory_id,),
        ).fetchone()

        return dict(row) if row is not None else None
    finally:
        connection.close()


def list_memories() -> list[dict]:
    """Return all memories, newest first with a deterministic tie-breaker."""
    connection = database.get_connection()
    try:
        rows = connection.execute(
            """
            SELECT id, content, memory_type, created_at, updated_at
            FROM memories
            ORDER BY created_at DESC, id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]
    finally:
        connection.close()
