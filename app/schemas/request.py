from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str
    model: str = "google/gemma-3-4b-it"
    stream: bool = True

