"""Embed platform outputs for evaluation or retrieval using the OpenAI Embeddings API.

Uses the openai.OpenAI client with the text-embedding-3-small model to
generate vector embeddings from text produced by the managed model platform.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from openai import OpenAI
from openai.types import CreateEmbeddingResponse

from model_client import create_openai_client, with_retry
from model_models import PlatformEmbeddingResponse

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def platform_output_embedding(
    text: str,
    client: Optional[OpenAI] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> PlatformEmbeddingResponse:
    """Generate an embedding for platform output text via the OpenAI Embeddings API.

    Args:
        text: The text to embed.
        client: Optional pre-configured OpenAI client.
        model: The OpenAI embedding model identifier.
        dimensions: Optional output dimensionality (e.g., 256, 512, 1024).

    Returns:
        A PlatformEmbeddingResponse with the embedding vector and metadata.
    """
    resolved_client = client or create_openai_client()

    payload: Dict[str, Any] = {
        "input": text,
        "model": model,
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions

    def _call() -> CreateEmbeddingResponse:
        return resolved_client.embeddings.create(**payload)

    response: CreateEmbeddingResponse = with_retry(_call)
    return PlatformEmbeddingResponse.from_openai_embedding(response)


def platform_output_embeddings_batch(
    texts: List[str],
    client: Optional[OpenAI] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> PlatformEmbeddingResponse:
    """Generate embeddings for a batch of platform output texts via OpenAI.

    The OpenAI embeddings.create endpoint accepts a list of strings as input.
    """
    resolved_client = client or create_openai_client()

    payload: Dict[str, Any] = {
        "input": texts,
        "model": model,
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions

    def _call() -> CreateEmbeddingResponse:
        return resolved_client.embeddings.create(**payload)

    response: CreateEmbeddingResponse = with_retry(_call)
    return PlatformEmbeddingResponse.from_openai_embedding(response)


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    import math

    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
