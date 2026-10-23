"""[SAME-SCENARIO] stream_platform_generation.py - streams output from a managed model platform while preserving provider response objects"""

import os
from model_client import get_managed_model_client
from model_models import StreamedGeneration


def stream_generation(
    deployment_id: str,
    prompt: str,
    chunk_size: int = 1024,
    **kwargs,
) -> StreamedGeneration:
    """
    Stream generation from the configured provider, yielding chunks as they become available.

    Args:
        deployment_id: Provider deployment identifier.
        prompt: Prompt text.
        chunk_size: Number of bytes/characters per yielded chunk.
        **kwargs: Additional provider‑specific parameters (e.g., temperature).

    Returns:
        A StreamedGeneration object containing the full output and original response metadata.
    """
    client = get_managed_model_client()
    # Assume client supports an async/generator ``stream`` method
    async_generator = client.stream(
        deployment_id=deployment_id,
        prompt=prompt,
        chunk_size=chunk_size,
        **kwargs,
    )
    # Collect chunks while preserving raw response objects
    chunks = []
    raw_resp = None
    async for chunk, resp in async_generator:
        chunks.append(chunk)
        raw_resp = resp  # keep the last response metadata object
    full_text = "".join(chunks)
    return StreamedGeneration(text=full_text, raw_response=raw_resp)
