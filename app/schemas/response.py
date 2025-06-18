from pydantic import BaseModel

class ChatResponse(BaseModel):
    results: dict
