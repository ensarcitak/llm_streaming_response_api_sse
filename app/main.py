from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.core.config import settings
from contextlib import asynccontextmanager
import logging
import uuid

logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting FastAPI with model: {settings.model_name}")
    yield
    logger.info("Shutting down FastAPI")

app = FastAPI(lifespan=lifespan, title="LLM Streaming API", version="1.0")

@app.middleware("http")
async def add_request_id_header(request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

app.include_router(api_router, prefix="/api")
