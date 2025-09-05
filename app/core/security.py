from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi import status, HTTPException

# nur um den Token aus dem Header zu extrahieren und Swagger/OpenAPI zu sagen wo es seinen eigenen token herholen kann
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

if os.path.exists(".env.dev"):
    load_dotenv(".env.dev")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# nur für validierung
class TokenData(BaseModel):
    username: str

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)    

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if not expires_delta:
        if ACCESS_TOKEN_EXPIRE_MINUTES:
            expires_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        else:
            expires_delta = timedelta(minutes=15)

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def exract_username_from_token(token : str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    return token_data.username



