import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt, JWTError

from pydantic import BaseModel

from sqlalchemy.orm import Session

from backend.security.hash import verify_password
from backend.database import get_db
from backend.models import user as user_model

# Generate SECRET_KEY with "openssl rand -hex 32"
SECRET_KEY = "SECRET"
ALGORITHM = "HS256"
EXP_MINUTE = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


def get_active_user(username: str, db: Session) -> user_model.User:
    user = db.query(user_model.User).filter(user_model.User.username == username, user_model.User.is_deleted == False).first()
    return user


def authenticate_user(username: str, password: str, db: Session):
    user = get_active_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(username: str):
    to_encode = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=EXP_MINUTE)
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username: str = payload.get("sub")
    except JWTError:
        raise credentials_exception
    user = get_active_user(username, db)
    if not user:
        raise credentials_exception
    return user


@router.post("/login", response_model=Token)
async def login_for_access_token(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form.username, form.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}
