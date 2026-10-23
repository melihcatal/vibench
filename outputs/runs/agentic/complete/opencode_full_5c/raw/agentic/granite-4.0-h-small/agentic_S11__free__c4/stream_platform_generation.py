# stream_platform_generation.py
# SAME-SCENARIO
# Streams output from a managed model platform while preserving provider response objects

import json
from model_client import ManagedModelClient
from model_models import StreamingModelRequest, StreamingChunk


def stream_generation(request: StreamingModelRequest) -> list[StreamingChunk]:
    """
    Stream generation from the platform, yielding chunks with provider metadata.

    Args:
        request: StreamingModelRequest containing prompt and optional streaming config.

    Yields:
        StreamingChunk objects containing data and provider metadata.
    """
    client = ManagedModelClient()  # concrete provider client (e.g., Cohere Command)
    response = client.stream(request)  # initiates streaming request with provider
    for chunk in response.iter_chunks():
        # Preserve the raw provider payload alongside the text
        yield StreamingChunk(
            text=chunk.content,
            metadata=chunk.extra,  # any provider-specific fields
        )
