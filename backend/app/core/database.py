
import sqlite3
from pathlib import Path

from app.core.config import settings


MEMORY_TYPES = ("learning", "project", "decision", "bug", "fix")


def get_database_path() -> Path:
    """Return the configured database path."""
    return settings.database_path


def get_connection() -> sqlite3.Connection:
    """Open a connection to the configured SQLite database."""
    database_path = get_database_path()

    # Create the parent directory if it does not exist.
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        database_path,
        timeout=10.0,
    )
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    """Create the memories table if it does not already exist."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL
                    CHECK (
                        length(trim(content)) > 0
                        AND length(content) <= 10000
                    ),
                memory_type TEXT NOT NULL
                    CHECK (
                        memory_type IN (
                            'learning',
                            'project',
                            'decision',
                            'bug',
                            'fix'
                        )
                    ),
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
