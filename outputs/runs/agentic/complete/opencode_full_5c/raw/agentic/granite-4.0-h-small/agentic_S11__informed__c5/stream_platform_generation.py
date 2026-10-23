# [SAME-SCENARIO] stream_platform_generation.py

from typing import AsyncIterator
from model_client import build_platform_model
from model_models import ManagedModelResponse


async def stream_platform_generation(
    request_id: str, response_iter: AsyncIterator[dict]
) -> AsyncIterator[ManagedModelResponse]:
    """Streams output from a managed model platform while preserving raw provider objects.

    Args:
        request_id (str): Identifier from the original ManagedModelResponse.
        response_iter: Async iterator of dicts as returned by the provider SDK
            (e.g., Vertex AI streaming generation).

    Yields:
        ManagedModelResponse: Each chunk wrapped as a normalized response with
                              the original provider payload attached.
    """
    async for chunk in response_iter:
        # Preserve the raw provider payload for downstream processing
        yield ManagedModelResponse(
            request_id=request_id,
            provider_payload=chunk,
            metadata={"status": "chunk-processed", "chunk_index": chunk.get("index")},
        )
