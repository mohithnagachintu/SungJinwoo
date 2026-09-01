from uuid import UUID

from fastapi import APIRouter, status

from fastapi_app.api.v1.task_queries import TaskListParamsDep
from fastapi_app.core.errors import TaskNotFoundError
from fastapi_app.core.pagination import PaginatedResponse
from fastapi_app.modules.tasks import store
from fastapi_app.modules.tasks.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> TaskRead:
    return store.create_task(payload)


@router.get("", response_model=PaginatedResponse[TaskRead])
def list_tasks(params: TaskListParamsDep) -> PaginatedResponse[TaskRead]:
    items, total = store.list_tasks_filtered(
        status=params.status,
        priority=params.priority,
        sort_by=params.sort_by,
        sort_direction=params.sort_direction.value,
        limit=params.limit,
        offset=params.offset,
    )
    return PaginatedResponse(
        items=items,
        total=total,
        limit=params.limit,
        offset=params.offset,
    )


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: UUID) -> TaskRead:
    task = store.get_task(task_id)
    if task is None:
        raise TaskNotFoundError()
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def patch_task(task_id: UUID, payload: TaskUpdate) -> TaskRead:
    task = store.update_task(task_id, payload)
    if task is None:
        raise TaskNotFoundError()
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID) -> None:
    if not store.delete_task(task_id):
        raise TaskNotFoundError()
