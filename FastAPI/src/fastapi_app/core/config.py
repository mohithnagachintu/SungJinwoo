from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        case_sensitive = False,
        extra = "ignore",
    )
    app_name: str = "TaskForge API"
    environment: Literal["local", "test", "staging", "production"] = "local"
    debug: bool = False

    database_url: PostgresDsn = Field(
        default = "postgresql+asyncpg://taskforge:taskforge@localhost:5432/taskforge"
    )

    cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory = lambda: ["http://localhost:3000"]
    )

    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    @field_validator("cors_origins", mode = "before")
    @classmethod
    def parse_cors_origin(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value
    
@lru_cache
def get_settings() -> Settings:
    return Settings()
    
