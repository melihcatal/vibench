import os
import json
from model_client import ManagedModelClient


def stream_platform_generation(resource_id: str, prompt: str) -> list[dict]:
    """Stream output from a managed model platform while preserving provider response objects.

    Args:
        resource_id: The concrete model/deployment/inference profile identifier.
        prompt: The user prompt to generate.

    Yields:
        Partial generation chunks as dicts containing content and provider metadata.
    """
    client = ManagedModelClient()
    # Use a streaming‑compatible provider method (e.g., Bedrock's chat completion)
    stream = client.stream(resource_id, prompt)
    for chunk in stream:
        # Each chunk contains raw provider data plus any extra context
        yield {
            "content": chunk.get("content"),
            "metadata": {
                "chunk_id": chunk.get("id"),
                "provider": client.service,
                "token_count": chunk.get("token_count"),
                "finish_reason": chunk.get("finish_reason"),
            },
        }
