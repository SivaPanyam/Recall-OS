
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import Settings
from app.core.logging_config import configure_logging


def test_configuration_defaults():
    settings = Settings(_env_file=None)

    assert settings.app_name == "OES - Personal AI Memory Engine"
    assert settings.app_version == "0.1.0"
    assert settings.environment == "development"
    assert settings.log_level == "INFO"
    assert settings.api_prefix == "/api/v1"
    assert settings.database_path == Path("data/oes.db")


def test_environment_variable_override(monkeypatch):
    monkeypatch.setenv("OES_ENV", "testing")

    settings = Settings(_env_file=None)

    assert settings.environment == "testing"


def test_database_path_environment_variable_override(monkeypatch):
    monkeypatch.setenv(
        "OES_DATABASE_PATH",
        "test_data/custom.db",
    )

    settings = Settings(_env_file=None)

    assert settings.database_path == Path("test_data/custom.db")


def test_invalid_log_level_is_rejected():
    settings = Settings(_env_file=None, log_level="INVALID")

    with patch("app.core.logging_config.settings", settings):
        with pytest.raises(ValueError, match="Invalid log level"):
            configure_logging()
