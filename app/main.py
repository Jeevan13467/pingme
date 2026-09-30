from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

from .database import Base, engine
from .routes import auth_routes, message_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Messaging App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(message_routes.router)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/chat")
def chat():
    return FileResponse(FRONTEND_DIR / "chat.html")

@app.get("/health")
def health():
    return {"status": "ok"}
