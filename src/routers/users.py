from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud
from ..database import get_db
from ..auth import get_current_active_user
from  ..middleware.exceptions import *

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=crud.User)
def create_user(user: crud.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user with the following information:
    - **email**: valid email address
    - **username**: unique username
    - **password**: secure password
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise UserAlreadyExistsException(user.email)
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[crud.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_active_user)
):
    """
    Get list of all users (requires authentication).
    - **skip**: number of records to skip
    - **limit**: maximum number of records to return
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/me", response_model=crud.User)
async def read_users_me(current_user: crud.User = Depends(get_current_active_user)):
    """
    Get current authenticated user information.
    """
    return current_user

@router.get("/{user_id}", response_model=crud.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise UserNotFoundException(user_id)
    return db_user