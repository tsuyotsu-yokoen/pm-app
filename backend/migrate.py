from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.security.hash import create_hashed_password
from backend.database import Base
from backend.models import (
    user as user_model,
    project as project_model,
    task as task_model
)

username = "app_admin"
password = "p@ssw0rd"
first = "User"
last = "Admin"
email = "admin@example.net"

DB_URL = "sqlite:///app.db"
engine = create_engine(url=DB_URL)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

with SessionLocal() as db:
    db.execute("PRAGMA foreign_keys = ON")

    user = user_model.User(
        username=username,
        password=create_hashed_password(password),
        first=first,
        last=last,
        email=email,
        created_by=username,
    )
    db.add(user)
    db.commit()
