from typing import Annotated, Literal

from fastapi import Depends, Query

from fastapi_app.core.pagination import SortDirection
from fastapi_app.modules.tasks.schemas import TaskPriority, TaskStatus

TaskSortField = Literal["created_at", "due_date", "priority", "status", "title"]


class TaskListParams:
    def __init__(
        self,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        sort_by: TaskSortField = Query(default="created_at"),
        sort_direction: SortDirection = SortDirection.DESC,
        limit: int = Query(default=20, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
    ) -> None:
        self.status = status
        self.priority = priority
        self.sort_by = sort_by
        self.sort_direction = sort_direction
        self.limit = limit
        self.offset = offset


TaskListParamsDep = Annotated[TaskListParams, Depends()]
