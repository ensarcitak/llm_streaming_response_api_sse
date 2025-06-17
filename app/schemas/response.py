from pydantic import BaseModel

class CompletionResponse(BaseModel):
    response: str