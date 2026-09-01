import os

from fastapi_app.core.config import Settings, get_settings


def test_default_settings():
    settings = Settings()

    assert settings.environment == "local"
    assert settings.debug is False
    assert settings.app_name == "TaskForge API"
    assert settings.access_token_expire_minutes == 30
    assert settings.refresh_token_expire_days == 7


def test_cors_origins_parsed_from_comma_separated_string():
    settings = Settings(cors_origins="http://a.com, http://b.com")

    assert settings.cors_origins == ["http://a.com", "http://b.com"]


def test_environment_override_from_env(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("DEBUG", "true")
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.environment == "test"
    assert settings.debug is True

    get_settings.cache_clear()