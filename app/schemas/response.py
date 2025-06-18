from pydantic import BaseModel

class TextResponse(BaseModel):
    response: str