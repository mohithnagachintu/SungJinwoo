from typing import Any

from fastapi import status

class AppError(Exception):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: list[dict[str,Any]] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, *, code: str, message: str = "Resource not found") -> None:
        super().__init__(
            code = code, 
            message = message,
            status_code = status.HTTP_404_NOT_FOUND,
        )
    
class ForbiddenError(AppError):
    def __init__(self, * , code: str = "FORBIDDEN", message: str = "Forbidden") -> None:
        super().__init__(
            code = code, 
            message = message, 
            status_code = status.HTTP_403_FORBIDDEN,
        )
    
class TaskNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(
            code = "TASK_NOT_FOUND",
            message = "Task not found",
        )