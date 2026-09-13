from sqlalchemy.orm import Session

from .. import models

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, hashed_password: str):
    user = models.User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session, exclude_username: str = None):
    query = db.query(models.User)
    if exclude_username:
        query = query.filter(models.User.username != exclude_username)
    return query.all()
