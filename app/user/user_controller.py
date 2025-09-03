from fastapi import Cookie, Depends, APIRouter, Request
from models import UserCreate, UserUpdate, UserPublic
from app.core.database import get_session
from typing import Annotated, Generator
from sqlmodel import Session




router = APIRouter()
db_session = Annotated[Session, Depends(get_session)]


@router.post("/users/", response_model=UserPublic)
def create_user(user: UserCreate, db : db_session):
    return user
