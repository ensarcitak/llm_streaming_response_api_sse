from typing import AsyncGenerator
from app.llm.ollama import OllamaClient
from app.core.config import settings

async def stream_tokens(prompt: str) -> AsyncGenerator[str, None]:
    """
    A token-by-token stream is obtained from Ollama for the prompt.    """
    client = OllamaClient()

    try:
        async for token in client.generate_stream(
            prompt=prompt,
            model=settings.model_name,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        ):
            yield token
    finally:
        await client.close()
