from pydantic import BaseModel


class User(BaseModel):
    first: str
    last: str

    class Config:
        orm_mode = True
