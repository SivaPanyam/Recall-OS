
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "OES - Personal AI Memory Engine"
    app_version: str = "0.1.0"
    environment: str = Field(
        default="development",
        validation_alias="OES_ENV",
    )
    log_level: str = "INFO"
    api_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_prefix="OES_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
