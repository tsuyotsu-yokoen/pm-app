from fastapi import FastAPI

from backend.security import oauth2
from backend.routers import user, project, task

app = FastAPI()

app.include_router(oauth2.router, tags=["OAuth2"])
app.include_router(user.router, tags=["User"], prefix="/api/v1")
app.include_router(project.router, tags=["Project"], prefix="/api/v1")
app.include_router(task.router, tags=["Task"], prefix="/api/v1")
