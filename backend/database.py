from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "sqlite:///backend/app.db"
engine = create_engine(url=DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def get_db():
    with SessionLocal() as db:
        db.execute("PRAGMA foreign_keys = ON")
        yield db


Base = declarative_base()
