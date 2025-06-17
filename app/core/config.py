# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_name: str = "gemma3:4b"
    temperature: float = 0.7
    max_tokens: int = 1024
    ollama_base_url: str = "http://127.0.0.1:11434"
    stream: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
