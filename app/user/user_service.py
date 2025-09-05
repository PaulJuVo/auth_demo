
from fastapi import status, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from app.user.user_models import *
from ..core import security 

    
def get_user_by_username(username: str, db : Session):
    try:
        user = db.exec(select(User).where(User.name == username)).one()
    except: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user

def create_user(user : UserCreate, db : Session):
    userDb = User.model_validate({**user.model_dump(),"hashedPassword": security.get_password_hash(user.password), "creationDate" : datetime.now()})
    try:
        db.add(userDb)
        db.commit()
        db.refresh(userDb)
    except:
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Conflict with Database"
    )
    return userDb





 