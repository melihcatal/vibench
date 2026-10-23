import os
from typing import AsyncGenerator

from model_client import GeminiClient
from model_models import StreamChunk, TextCompletionRequest


async def stream_completion(
    prompt: str, model_name: str = "gemini-pro", temperature: float = 0.7
) -> AsyncGenerator[StreamChunk, None]:
    """Streams partial output tokens from a hosted LLM."""
    client = GeminiClient()
    request = TextCompletionRequest(
        prompt=prompt,
        model_name=model_name,
        max_output_tokens=1000,
        temperature=temperature,
    )
    async for chunk in client.stream_completion(request):
        yield chunk
