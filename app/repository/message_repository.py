from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from .. import models

def create_message(db: Session, sender_id: int, receiver_id: int, content: str):
    message = models.Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_conversation(db: Session, user_a_id: int, user_b_id: int):
    return (
        db.query(models.Message)
        .filter(
            or_(
                and_(models.Message.sender_id == user_a_id, models.Message.receiver_id == user_b_id),
                and_(models.Message.sender_id == user_b_id, models.Message.receiver_id == user_a_id),
            )
        )
        .order_by(models.Message.timestamp.asc())
        .all()
    )
