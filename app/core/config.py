from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_id: str = "google/gemma-1.1-4b-it"
    temperature: float = 0.6
    max_new_tokens: int = 1024
    device: str = "cuda"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
