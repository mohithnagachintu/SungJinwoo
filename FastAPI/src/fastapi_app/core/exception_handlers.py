from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from fastapi_app.core.errors import AppError
from fastapi_app.core.responses import ErrorBody, ErrorResponse

def app_error_handler(_request: Request, 
                      exc: AppError) -> JSONResponse:
    payload = ErrorResponse(
        error = ErrorBody(
            code = exc.code,
            message = exc.message,
            details = exc.details,
        )
    )
    return JSONResponse(
        status_code = exc.status_code,
        content = payload.model_dump(
            exclude_none = True
        ),
    )

def validation_error_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    details = [
        {
            "field" : ".".join(str(part) for part in error["loc"] if part != "body"),
            "message" : error["msg"],
            "type" : error["type"],
        }
        for error in exc.errors()
    ]

    payload = ErrorResponse(
        error = ErrorBody(
            code = "VALIDATION_ERROR",
            message = "Request validation failed",
            details = details,
        )
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content = payload.model_dump(
            exclude_none = True,
        )
    )