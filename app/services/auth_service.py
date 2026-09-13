from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import auth
from ..repository import user_repository

def register_user(db: Session, username: str, password: str):
    existing = user_repository.get_user_by_username(db, username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed = auth.hash_password(password)
    return user_repository.create_user(db, username, hashed)

def authenticate_user(db: Session, username: str, password: str):
    user = user_repository.get_user_by_username(db, username)
    if not user or not auth.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return user
