from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from fastapi_app.api.router import router as api_router
from fastapi_app.core.config import get_settings

from fastapi_app.core.errors import AppError
from fastapi_app.core.exception_handlers import (
    app_error_handler,
    validation_error_handler
)

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title = settings.app_name,
        version = "0.1.0",
        description = "Multi-user project and task management backend.",
        debug = settings.debug,
    )

    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)

    app.include_router(api_router)
    return app