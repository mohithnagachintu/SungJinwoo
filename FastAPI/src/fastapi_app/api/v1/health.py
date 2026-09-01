from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter(tags = ["health"])

class HealthResponse(BaseModel):
    status: str

class ReadyResponse(BaseModel):
    status: str
    checks: dict[str, str]

@router.get("/health", response_model = HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status = "ok")

@router.get("/ready", response_model = ReadyResponse)
def readiness_check() -> ReadyResponse:
    return ReadyResponse(
        status = "ok",
        checks = {
            "app": "ok",
            "database": "ok",    # this is will be real check later
        }
    )