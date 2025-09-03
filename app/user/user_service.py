

from sqlmodel import Session, select

from app.user.user_models import User


def get_user_by_username(username: str, db : Session):
    if username:
        user = db.exec(select(User).where(username == username)).one()
        if user: 
            return user


