from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router as api_router
from app.core.logging import Logger
# Initialize logger
logger = Logger(__name__)


# Initialize FastAPI application
logger.info("Initializing FastAPI application...")
app = FastAPI(title="LLM Streaming API (Huggingface model based)", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api")
