from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/health")
def health():
    return {"status": "ok"}
