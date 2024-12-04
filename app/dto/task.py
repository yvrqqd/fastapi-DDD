from enum import Enum

from pydantic import BaseModel


__all__ = (
    'TaskStatus',
    'CreateTaskRequest',
    'CreateTaskResponse',
    'ReadTaskResponse',
    'ReadTaskListRequest',
    'UpdateTaskRequest',
    'UpdateTaskResponse',
    'DeleteTaskResponse',
)


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class BaseResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus


class CreateTaskRequest(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO


class CreateTaskResponse(BaseResponse):
    pass


class ReadTaskResponse(BaseResponse):
    pass


class ReadTaskListRequest(BaseModel):
    status: TaskStatus | None = None


class UpdateTaskRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None


class UpdateTaskResponse(BaseResponse):
    pass


class DeleteTaskResponse(BaseModel):
    id: int


