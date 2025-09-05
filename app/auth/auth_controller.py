from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .auth_service import authenticate_user, Token
from typing import Annotated
from ..core.security import create_access_token
from ..core.deps import db_session



router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db : db_session
) -> Token:
    authenticate_user(form_data.username, form_data.password, db)
    access_token = create_access_token(data={"sub": form_data.username})
    return Token(access_token=access_token, token_type="bearer")

