from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship

from backend.database import Base


class TaskMember(Base):
    __tablename__ = "task_members"

    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    username = Column(String, ForeignKey("users.username"), primary_key=True)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime)
    is_completed = Column(Boolean, nullable=False, default=False)
    created_by = Column(String, ForeignKey("users.username"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=current_timestamp())
    updated_by = Column(String, ForeignKey("users.username"))
    updated_at = Column(DateTime, onupdate=current_timestamp())

    members = relationship(
        "User",
        secondary=TaskMember.__tablename__,
        back_populates="tasks"
    )

    created_by_user = relationship("User", foreign_keys=[created_by])
    updated_by_user = relationship("User", foreign_keys=[updated_by])
