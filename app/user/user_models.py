from sqlmodel import Field, SQLModel
from datetime import datetime

class BaseUser(SQLModel):
    name : str = Field(index=True, unique=True)
    age: int | None
    
class User(BaseUser, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashedPassword: str
    creationDate : datetime

class UserCreate(BaseUser):
    password : str

class UserUpdate(BaseUser):
    name : str | None 
    age: int | None
    password: int | None

class UserPublic(BaseUser):
    id: int | None