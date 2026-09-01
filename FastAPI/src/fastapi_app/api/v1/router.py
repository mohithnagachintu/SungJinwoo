from fastapi import APIRouter

from fastapi_app.api.v1 import health, tasks

router = APIRouter(prefix = "/api/v1")
router.include_router(health.router)
router.include_router(tasks.router)
