import httpx
import asyncio
from typing import AsyncGenerator, Optional
from app.core.config import settings

class OllamaClient:
    def __init__(self, base_url: str = settings.ollama_base_url):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=None)  # timeout=None for long streaming

    async def generate_stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Token-by-token stream halinde cevap üretir.
        """
        model = model or settings.model_name
        temperature = temperature or settings.temperature
        max_tokens = max_tokens or settings.max_tokens

        url = f"/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }

        async with self.client.stream("POST", url, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line.removeprefix("data: ").strip()
                    if data == "[DONE]":
                        break
                    yield data

    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Synchronous-like single full response generation.
        """
        model = model or settings.model_name
        temperature = temperature or settings.temperature
        max_tokens = max_tokens or settings.max_tokens

        url = f"/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }

        async with self.client as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            json_resp = response.json()
            return json_resp.get("response", "")  # Use "response" field instead of "choices"        

    async def close(self):
        await self.client.aclose()
