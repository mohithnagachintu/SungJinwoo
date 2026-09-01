from datetime import datetime, UTC
from enum import StrEnum
from multiprocessing import Value
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"

class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskCreate(BaseModel):
    title: str = Field(min_length = 1, max_length = 200)
    description: str | None = Field(default = None, max_length = 2000)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None

    @field_validator("due_date")
    @classmethod
    def due_date_cannot_be_in_past(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value
        
        # Normalize to UTC for comparison
        due = value if value.tzinfo else value.replace(tzinfo = UTC)
        if due < datetime.now(UTC):
            raise ValueError("Due date cannot be in the past")
        return value

class TaskUpdate(BaseModel):
    title: str | None = Field (default = None, min_length = 1, max_length = 200)
    description: str | None = Field (default = None, max_length = 2000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None

    @field_validator("due_date")
    @classmethod
    def due_date_cannot_be_in_past(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value
        
        # Normalize to UTC for comparison
        due = value if value.tzinfo else value.replace(tzinfo = UTC)
        if due < datetime.now(UTC):
            raise ValueError("Due date cannot be in the past")
        return value

class TaskRead(BaseModel):
    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}