from pydantic import BaseModel
from fastapi import Form
from typing import Optional

class ChatRequest(BaseModel):
    prompt: str
    model: str = "google/gemma-3-4b-it"
    stream: bool = True

    @classmethod
    def as_form(
        cls,
        prompt: str = Form(...),
        model: str = Form("google/gemma-3-4b-it"),
        stream: bool = Form(True)
    ):
        return cls(
            prompt=prompt,
            model=model,
            stream=stream
        )

