import datetime

from pydantic import BaseModel
from typing import List, Optional

from backend.schemas import (
    project as project_schema,
    task as task_schema
)
from backend.schemas.utils import User


class UserBase(BaseModel):
    first: str
    last: str
    email: str


class UserCreate(UserBase):
    username: str
    password: str


class UserUpdate(UserBase):
    password: str


class UserResponse(UserBase):
    username: str
    is_deleted: bool
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None

    projects: List[project_schema.ProjectResponse]
    tasks: List[task_schema.TaskResponse]

    created_by_user: User
    updated_by_user: Optional[User] = None

    class Config:
        orm_mode = True
