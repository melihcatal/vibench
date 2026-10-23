import json
from typing import Iterator, Any
from model_client import ManagedModelClient
from model_models import ModelStreamingResponse


def stream_platform_generation(
    project_id: str,
    deployment_id: str,
    payload: dict,
    chunk_callback: callable = None,
) -> ModelStreamingResponse:
    """Streams generation output from a managed model platform while preserving provider response objects.

    Args:
        project_id: Project identifier scoped to the provider.
        deployment_id: Deployment or inference profile identifier.
        payload: Request payload (e.g., prompt, temperature, etc.).
        chunk_callback: Optional callable that receives each raw chunk as it arrives.

    Returns:
        A ModelStreamingResponse containing the complete streamed output and metadata.
    """
    client = ManagedModelClient()
    # Provider‑specific streaming method – here we assume a method called `stream_generate`
    stream_resp = client.stream_generate(
        project_id=project_id,
        deployment_id=deployment_id,
        payload=payload,
    )
    # Accumulate raw chunks and forward to callback if supplied
    accumulated_chunks = []
    for raw_chunk in stream_resp.iter_chunks():
        accumulated_chunks.append(raw_chunk)
        if chunk_callback:
            chunk_callback(raw_chunk)
    # Return a structured response that also stores raw provider metadata
    return ModelStreamingResponse(
        chunks=accumulated_chunks,
        metadata=stream_resp.metadata,
    )
