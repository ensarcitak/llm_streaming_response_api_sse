from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional, Union
import os


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LLM Streaming API (Huggingface model based)"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "An API for streaming responses from LLMs using Huggingface models."
    
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3002"]

    HUGGINGFACE_API_KEY: Optional[str] = os.getenv("HUGGINGFACE_API_KEY", None)
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()