from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.security.oauth2 import get_current_user
from backend.database import get_db
from backend.cruds import task as task_crud
from backend.schemas import (
    task as task_schema,
    user as user_schema
)

router = APIRouter()


@router.post("/tasks", response_model=task_schema.TaskResponse)
async def create(
        task_in: task_schema.TaskCreate,
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return task_crud.create(task_in, db, current_user)


@router.get("/tasks/{task_id", response_model=task_schema.TaskResponse)
async def read(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return task_crud.read(task_id, db)


@router.get("/tasks", response_model=List[task_schema.TaskResponse])
async def reads(
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return task_crud.reads(db)


@router.put("/tasks/{task_id", response_model=task_schema.TaskResponse)
async def update(
        task_id: int,
        task_in: task_schema.TaskUpdate,
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return task_crud.update(task_id, task_in, db, current_user)


@router.delete("/tasks/{task_id}", response_model=task_schema.TaskResponse)
async def delete(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return task_crud.delete(task_id, db, current_user)
