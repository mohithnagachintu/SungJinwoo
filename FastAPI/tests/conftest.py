import pytest
from fastapi.testclient import TestClient

from fastapi_app.app import create_app
from fastapi_app.core.config import Settings, get_settings

@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        environment="test",
        debug=True,
        database_url="postgresql+asyncpg://taskforge:taskforge@localhost:5432/taskforge_test",
        cors_origins=["http://testserver"],
    )

@pytest.fixture
def client(test_settings: Settings) -> TestClient:
    get_settings.cache_clear()
    app = create_app()

    app.dependency_overrides[get_settings] = lambda: test_settings

    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
    get_settings.cache_clear()
