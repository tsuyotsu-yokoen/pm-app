from sqlalchemy.orm import Session
from typing import List

from backend.security.hash import create_hashed_password
from backend.models import user as user_model
from backend.schemas import user as user_schema


def create(user_in: user_schema.UserCreate, db: Session, current_user: user_schema.UserResponse):
    user = user_model.User(
        username=user_in.username,
        password=create_hashed_password(user_in.password),
        first=user_in.first,
        last=user_in.last,
        email=user_in.email,
        created_by=current_user.username
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def read(username: str, db: Session) -> user_model.User:
    return db.query(user_model.User).filter(user_model.User.username == username).first()


def reads(db: Session) -> List[user_model.User]:
    return db.query(user_model.User).all()


def update(username: str, user_in: user_schema.UserUpdate, db: Session, current_user: user_schema.UserResponse):
    user = read(username, db)
    user.password = create_hashed_password(user_in.password)
    user.first = user_in.first
    user.last = user_in.last
    user.email = user_in.email
    user.updated_by = current_user.username
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete(username: str, db: Session, current_user: user_schema.UserResponse):
    user = read(username, db)
    user.is_deleted = True
    user.updated_by = current_user.username
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
