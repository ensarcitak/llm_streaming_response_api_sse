from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
from app.schemas.request import PromptRequest
from app.schemas.response import CompletionResponse
from app.llm.ollama import OllamaClient
from app.llm.stream import stream_tokens

router = APIRouter()

@router.post("/sync", response_model=CompletionResponse)
async def sync_completion(payload: PromptRequest):
    """
    Synchronous endpoint that returns a complete response to the client.
    This endpoint is not streaming and returns the full response at once.
    """
    client = OllamaClient()
    try:
        response = await client.generate(prompt=payload.prompt)
        return CompletionResponse(response=response)
    finally:
        await client.close()

@router.post("/stream")
async def stream_completion(payload: PromptRequest):
    """
    Streaming endpoint that responds token-by-token to client.
    SSE (Server-Sent Events) format.
    """

    async def event_generator():
        async for token in stream_tokens(payload.prompt):
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")