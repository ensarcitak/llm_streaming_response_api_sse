from pydantic import BaseModel, Field

class PromptRequest(BaseModel):
    prompt: str = Field(..., description="The user prompt to send to the LLM.")