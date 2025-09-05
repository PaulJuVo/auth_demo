from fastapi import status, HTTPException
import os
from dotenv import load_dotenv
from sqlmodel import Session
from pydantic import BaseModel
from ..core import security
from ..user.user_service import get_user_by_username


if os.path.exists(".env.dev"):
    load_dotenv(".env.dev")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")




class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username : str, password : str, db : Session):
    user = get_user_by_username(username, db)
    if user and security.verify_password(password, user.hashedPassword):
        return True
    else: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    