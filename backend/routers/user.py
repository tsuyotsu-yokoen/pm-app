from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.security.oauth2 import get_current_user
from backend.database import get_db
from backend.cruds import user as user_crud
from backend.schemas import user as user_schema

router = APIRouter()


@router.post("/users", response_model=user_schema.UserResponse)
async def create(
        user_in: user_schema.UserCreate,
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return user_crud.create(user_in, db, current_user)


@router.get("/users/{username}", response_model=user_schema.UserResponse)
async def read(
        username: str,
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return user_crud.read(username, db)


@router.get("/users", response_model=List[user_schema.UserResponse])
async def reads(
    db: Session = Depends(get_db),
    current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return user_crud.reads(db)


@router.put("/users/{username}", response_model=user_schema.UserResponse)
async def update(
        username: str,
        user_in: user_schema.UserUpdate,
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return user_crud.update(username, user_in, db, current_user)


@router.delete("/users/{username}", response_model=user_schema.UserResponse)
async def delete(
        username: str,
        db: Session = Depends(get_db),
        current_user: user_schema.UserResponse = Depends(get_current_user)
):
    return user_crud.delete(username, db, current_user)
