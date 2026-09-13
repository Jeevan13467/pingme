from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MessageCreate(BaseModel):
    receiver_username: str
    content: str

class MessageOut(BaseModel):
    id: int
    sender_username: str
    receiver_username: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True
