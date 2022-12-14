from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.security.oauth2 import get_current_user
from backend.database import get_db
from backend.cruds import project as project_crud
from backend.schemas import (
    project as project_schema,
    user as user_schema
)

router = APIRouter()


@router.post("/projects", response_model=project_schema.ProjectResponse)
async def create(
        project_in: project_schema.ProjectCreate,
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return project_crud.create(project_in, db, current_user)


@router.get("/projects/{project_id}", response_model=project_schema.ProjectResponse)
async def read(
        project_id: int,
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return project_crud.read(project_id, db)


@router.get("/projects", response_model=List[project_schema.ProjectResponse])
async def reads(
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return project_crud.reads(db)


@router.put("/projects/{project_id}", response_model=project_schema.ProjectResponse)
async def update(
        project_id: int,
        project_in: project_schema.ProjectUpdate,
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return project_crud.update(project_id, project_in, db, current_user)


@router.delete("/projects/{project_id}", response_model=project_schema.ProjectResponse)
async def delete(
        project_id: int,
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return project_crud.delete(project_id, db, current_user)
