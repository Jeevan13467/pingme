from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..repository import message_repository, user_repository

def send_message(db: Session, sender, receiver_username: str, content: str):
    receiver = user_repository.get_user_by_username(db, receiver_username)
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient not found")
    if receiver.id == sender.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot message yourself")
    return message_repository.create_message(db, sender.id, receiver.id, content)

def get_conversation(db: Session, user, other_username: str):
    other = user_repository.get_user_by_username(db, other_username)
    if not other:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return message_repository.get_conversation(db, user.id, other.id)
