from typing import AsyncIterator
import httpx
from model_client import LLMClient
from model_models import LLMRequest, StreamChunk, normalize_stream_chunk


async def stream_completion(prompt: str) -> AsyncIterator[str]:
    """Stream partial output tokens from Mistral's hosted LLM."""
    client = LLMClient()
    request = LLMRequest(prompt=prompt, max_tokens=1000)

    response = await client.stream(
        request.prompt, request.temperature, request.max_tokens
    )
    async for chunk in response.aiter_bytes():
        chunk_str = chunk.decode("utf-8")
        normalized = normalize_stream_chunk(chunk_str)
        if normalized and normalized.choices:
            yield normalized.choices[0]["delta"]["content"]

    await client.close()
