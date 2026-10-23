# [SAME-SCENARIO] stream_platform_generation.py
import os
from model_client import ManagedModelClient
from model_models import ModelStreamInvocationRequest, StreamResponseChunk

def stream_platform_generation(deployment_id: str, prompt: str) -> list[StreamResponseChunk]:
    """Stream output from a managed model while preserving provider response objects.

    Uses the client's streaming endpoint (e.g., OpenAI's chat/completions streaming) and returns each chunk
    together with its raw provider container so callers can inspect latency, token counts, etc.
    """
    client = ManagedModelClient()
    request = ModelStreamInvocationRequest(
        deployment_id=deployment_id,
        prompt=prompt,
        temperature=0.7,
        # other streaming parameters could be added
    )
    chunks = []
    async for chunk in client.stream(request):
        # chunk.raw contains the untouched provider payload (e.g., dict with 'choices', 'usage', ...)
        chunks.append(StreamResponseChunk(text=chunk.text, raw=chunk.raw))
    return chunks
