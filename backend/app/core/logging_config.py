
import logging

from app.core.config import settings


def configure_logging() -> None:
    """Configure application-wide console logging."""

    level = getattr(logging, settings.log_level.upper(), None)

    if not isinstance(level, int):
        raise ValueError(
            f"Invalid log level: {settings.log_level}"
        )

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )
