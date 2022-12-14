import datetime

from pydantic import BaseModel
from typing import List, Optional

from backend.schemas.utils import User


class TaskBase(BaseModel):
    title: str
    content: Optional[str] = None
    start_datetime: datetime.datetime
    end_datetime: Optional[datetime.datetime] = None


class TaskCreate(TaskBase):
    project_id: int
    member_usernames: List[str]


class TaskUpdate(TaskBase):
    member_usernames: List[str]


class TaskResponse(TaskBase):
    id: int
    project_id: int
    is_completed: bool

    members: List[User]

    created_by_user: User
    updated_by_user: Optional[User] = None

    class Config:
        orm_mode = True
