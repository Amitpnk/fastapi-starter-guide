from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings, read from environment variables or a `.env` file.

    Example: set `APP_NAME="My API"` to override `app_name`.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "FastAPI Starter"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
