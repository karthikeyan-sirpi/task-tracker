from pydantic import BaseModel
from uuid import UUID


class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: UUID