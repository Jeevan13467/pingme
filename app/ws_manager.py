from typing import Dict

from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, username: str):
        self.active_connections.pop(username, None)

    async def send_to_user(self, username: str, message: dict):
        websocket = self.active_connections.get(username)
        if websocket:
            await websocket.send_json(message)

manager = ConnectionManager()
