from fastapi import APIRouter
from app.api.endpoints import health_check, chat

router = APIRouter()

router.include_router(health_check.router, prefix="/health", tags=["Health Check"])
router.include_router(chat.router, prefix="/chat", tags=["Chat"])