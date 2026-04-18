"""
Application configuration loaded from environment variables.

Uses Pydantic BaseSettings for type-safe, validated config.
All secrets are read from a `.env` file — never hardcoded.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central settings object.

    Attributes:
        APP_NAME:      Display name used in docs and health checks.
        APP_VERSION:   Semantic version string.
        DEBUG:         Toggle debug mode (extra logging, detailed errors).
        SUPABASE_URL:  Full URL of your Supabase project (e.g. https://xyz.supabase.co).
        SUPABASE_KEY:  Anon or service-role key for Supabase.
    """

    APP_NAME: str = "CampusTrade API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    SUPABASE_URL: str
    SUPABASE_KEY: str

    # Pydantic v2 config — reads from .env automatically
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    Using @lru_cache ensures the .env file is read only once,
    and the same Settings object is reused across the app lifetime.
    """
    return Settings()
