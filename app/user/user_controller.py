from fastapi import APIRouter
from .user_service import create_user as user_service_create_user
from .user_models import *
from ..core.deps import CurrentUser


router = APIRouter()


@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate):
    
    return user_service_create_user(user)

@router.get("/me/", response_model=UserPublic)
def get_user(user : CurrentUser):
    return user

@router.get("/all/", response_model=UserPublic)
def get_all_users(user : CurrentUser):
    return user
    