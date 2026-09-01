from datetime import UTC, datetime
from uuid import UUID, uuid4

from fastapi_app.modules.tasks.schemas import TaskStatus, TaskCreate, TaskPriority, TaskRead, TaskUpdate

_tasks: dict[UUID, TaskRead] = {}

ALLOWED_SORT_FIELDS = {"created_at", "due_date", "priority", "status", "title"}

def create_task(payload: TaskCreate) -> TaskRead:
    now = datetime.now(UTC)
    task = TaskRead(
        id = uuid4(),
        title = payload.title,
        description = payload.description,
        status = payload.status,
        priority = payload.priority,
        due_date = payload.due_date,
        created_at = now,
        updated_at = now,
    )
    _tasks[task.id] = task
    return task

def list_tasks() -> list[TaskRead]:
    return list(_tasks.values())

def list_tasks_filtered(
    *,
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    sort_by: str = "created_at",
    sort_direction: str = "desc",
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[TaskRead], int]:
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [t for t in tasks if t.status == status]
    if priority is not None:
        tasks = [t for t in tasks if t.priority == priority]
    
    reverse = sort_direction == "desc"
    tasks.sort(key = lambda t: getattr(t, sort_by), reverse = reverse)
    total = len(tasks)
    return tasks[offset : offset + limit], total

def get_task(task_id: UUID) -> TaskRead | None:
    return _tasks.get(task_id)

def update_task(task_id: UUID, payload: TaskUpdate) -> TaskRead | None:
    task = _tasks.get(task_id)
    if task is None:
        return None
    updates = payload.model_dump(exclude_unset=True)
    updated = task.model_copy(update={**updates, "updated_at": datetime.now(UTC)})
    _tasks[task_id] = updated
    return updated

def delete_task(task_id: UUID) -> bool:
    return _tasks.pop(task_id, None) is not None

