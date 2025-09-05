from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from app.core.database import get_session
from app.user.user_models import User
from app.user.user_service import get_user_by_username

from .security import exract_username_from_token

from fastapi.security import OAuth2PasswordBearer
# nur um den Token aus dem Header zu extrahieren und Swagger/OpenAPI zu sagen wo es seinen eigenen token herholen kann
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# DB Session Dependency
db_session = Annotated[Session, Depends(get_session)]

def get_user_from_token(token : Annotated[str, Depends(oauth2_scheme)], db : db_session):
    username = exract_username_from_token(token)
    return get_user_by_username(username, db)
    
# Current User Dependency
CurrentUser = Annotated[User, Depends(get_user_from_token)]