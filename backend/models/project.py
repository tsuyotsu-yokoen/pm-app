from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship

from backend.database import Base


class ProjectMember(Base):
    __tablename__ = "project_members"

    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    username = Column(String, ForeignKey("users.username"), primary_key=True)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    is_completed = Column(Boolean, nullable=False, default=False)
    created_by = Column(String, ForeignKey("users.username"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=current_timestamp())
    updated_by = Column(String, ForeignKey("users.username"))
    updated_at = Column(DateTime, onupdate=current_timestamp())

    members = relationship(
        "User",
        secondary=ProjectMember.__tablename__,
        back_populates="projects"
    )

    tasks = relationship("Task")

    created_by_user = relationship("User", foreign_keys=[created_by])
    updated_by_user = relationship("User", foreign_keys=[updated_by])
