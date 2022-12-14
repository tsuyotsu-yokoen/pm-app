from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.models import (
    project as project_model,
    task as task_model
)

remen
class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    first = Column(String, nullable=False)
    last = Column(String, nullable=False)
    email = Column(String, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_by = Column(String, ForeignKey("users.username"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=current_timestamp())
    updated_by = Column(String, ForeignKey("users.username"))
    updated_at = Column(DateTime, onupdate=current_timestamp())

    projects = relationship(
        "Project",
        secondary=project_model.ProjectMember.__tablename__,
        back_populates="members"
    )

    tasks = relationship(
        "Task",
        secondary=task_model.TaskMember.__tablename__,
        back_populates="members"
    )

    created_by_user = relationship("User", foreign_keys=[created_by], remote_side=[username])
    updated_by_user = relationship("User", foreign_keys=[updated_by], remote_side=[username])
