from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from .. import auth, schemas
from ..database import get_db
from ..repository import user_repository
from ..services import message_service
from ..ws_manager import manager

router = APIRouter(tags=["messages"])

@router.get("/users", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return user_repository.list_users(db, exclude_username=current_user.username)

@router.post("/messages", response_model=schemas.MessageOut)
async def send_message(msg: schemas.MessageCreate, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    message = message_service.send_message(db, current_user, msg.receiver_username, msg.content)
    await manager.send_to_user(
        msg.receiver_username,
        {
            "sender": current_user.username,
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
        },
    )
    return message

@router.get("/messages/{other_username}", response_model=List[schemas.MessageOut])
def get_conversation(other_username: str, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return message_service.get_conversation(db, current_user, other_username)

@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(username, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(username)
