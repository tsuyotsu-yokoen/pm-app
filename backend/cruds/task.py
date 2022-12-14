from sqlalchemy.orm import Session

from backend.models import task as task_model
from backend.cruds import user as user_crud
from backend.schemas import (
    task as task_schema,
    user as user_schema
)


def create(task_in: task_schema.TaskCreate, db: Session, current_user: user_schema.UserResponse):
    task = task_model.Task(
        project_id=task_in.project_id,
        title=task_in.title,
        content=task_in.content,
        start_datetime=task_in.start_datetime,
        end_datetime=task_in.end_datetime,
        created_by=current_user.username
    )

    for username in task_in.member_usernames:
        user = user_crud.read(username, db)
        task.members.append(user)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def read(task_id: int, db: Session) -> task_model.Task:
    return db.query(task_model.Task).filter(task_model.Task.id == task_id).first()


def reads(db: Session):
    return db.query(task_model.Task).all()


def update(task_id: int, task_in: task_schema.TaskUpdate, db: Session, current_user: user_schema.UserResponse):
    task = read(task_id, db)
    task.title = task_in.title
    task.content = task_in.content
    task.start_datetime = task_in.start_datetime
    task.end_datetime = task_in.end_datetime
    task.updated_by = current_user.username

    task.members.clear()

    for username in task_in.member_usernames:
        user = user_crud.read(username, db)
        task.members.append(user)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete(task_id: int, db: Session, current_user: user_schema.UserResponse):
    task = read(task_id, db)
    task.is_completed = True
    task.updated_by = current_user.username
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
