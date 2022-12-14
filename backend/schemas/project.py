import datetime

from pydantic import BaseModel
from typing import List, Optional

from backend.schemas import task as task_schema
from backend.schemas.utils import User


class ProjectBase(BaseModel):
    title: str
    content: str
    start_date: datetime.date
    end_date: Optional[datetime.date] = None


class ProjectCreate(ProjectBase):
    member_usernames: List[str]


class ProjectUpdate(ProjectBase):
    member_usernames: List[str]


class ProjectResponse(ProjectBase):
    id: int
    is_completed: bool

    members: List[User]

    tasks: List[task_schema.TaskResponse]

    created_by_user: User
    updated_by_user: Optional[User] = None

    class Config:
        orm_mode = True
