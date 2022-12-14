from sqlalchemy.orm import Session

from backend.models import project as project_model
from backend.cruds import user as user_crud
from backend.schemas import (
    project as project_schema,
    user as user_schema
)


def create(project_in: project_schema.ProjectCreate, db: Session, current_user: user_schema.UserResponse):
    project = project_model.Project(
        title=project_in.title,
        content=project_in.content,
        start_date=project_in.start_date,
        end_date=project_in.end_date,
        created_by=current_user.username
    )

    for username in project_in.member_usernames:
        user = user_crud.read(username, db)
        project.members.append(user)

    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def read(project_id: int, db: Session) -> project_model.Project:
    return db.query(project_model.Project).filter(project_model.Project.id == project_id).first()


def reads(db: Session):
    return db.query(project_model.Project).all()


def update(project_id: int, project_in: project_schema.ProjectUpdate, db: Session, current_user: user_schema.UserResponse):
    project = read(project_id, db)
    project.title = project_in.title
    project.content = project_in.content
    project.start_date = project_in.start_date
    project.end_date = project_in.end_date
    project.updated_by = current_user.username

    project.members.clear()

    for username in project_in.member_usernames:
        user = user_crud.read(username, db)
        project.members.append(user)

    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def delete(project_id: int, db: Session, current_user: user_schema.UserResponse):
    project = read(project_id, db)
    project.is_completed = True
    project.updated_by = current_user.username
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
