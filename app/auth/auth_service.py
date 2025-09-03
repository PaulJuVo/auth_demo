from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from sqlmodel import Session

from app.user.user_service import get_user_by_username
from app.auth import *

if os.path.exists(".env.dev"):
    load_dotenv(".env.dev")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# nur um den Token aus dem Header zu extrahieren und Swagger/OpenAPI zu sagen wo es seinen eigenen token herholen kann
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db : Session, username : str, password : str):
    user = get_user_by_username(username, db)
    if (user & verify_password(password, user.hashedPassword)):
        return True
    return False
    

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

