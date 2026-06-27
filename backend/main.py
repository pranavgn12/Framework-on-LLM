from fastapi import FastAPI
from routers import auth
from database import engine
from models import Base
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import chats
from routers import messages
from auth_utils import get_current_user

# Create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mental Health Chatbot API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    chats.router,
    prefix="/chats",
    tags=["Chats"]
)

app.include_router(
    messages.router,
    prefix="/messages",
    tags=["Messages"]
)

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Mental Health Chatbot Backend"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.get("/me")
def me(
    user=Depends(get_current_user)
):
    return user

