"""
embeddings_client.py - Local configuration and client helper utilities for Direct Embeddings API.

Provider: OpenAI Embeddings API (text-embedding-3-small, text-embedding-3-large)
SDK: openai
Auth: OPENAI_API_KEY environment variable
"""

import os
from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_LARGE_MODEL = "text-embedding-3-large"

_api_key = os.environ.get("OPENAI_API_KEY", "")


def get_openai_client() -> OpenAI:
    """Create and return an authenticated OpenAI client instance."""
    if not _api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for OpenAI Embeddings API."
        )
    return OpenAI(api_key=_api_key)


def resolve_model(model_name: str | None = None) -> str:
    """Resolve the embedding model identifier, defaulting to text-embedding-3-small."""
    if model_name:
        return model_name
    return os.environ.get("OPENAI_EMBEDDING_MODEL", OPENAI_EMBEDDING_MODEL)


def chunk_texts(texts: list[str], max_batch_size: int = 50) -> list[list[str]]:
    """Split a list of texts into batches respecting OpenAI batch size limits."""
    chunks: list[list[str]] = []
    for i in range(0, len(texts), max_batch_size):
        chunks.append(texts[i : i + max_batch_size])
    return chunks


def validate_embedding_response(response: dict | object) -> list[list[float]]:
    """Extract embedding vectors from an OpenAI embeddings API response."""
    if hasattr(response, "data"):
        data = response.data
    elif isinstance(response, dict):
        data = response.get("data", [])
    else:
        raise ValueError("Unexpected response format from OpenAI Embeddings API")

    embeddings: list[list[float]] = []
    for item in sorted(data, key=lambda x: x.index):
        if hasattr(item, "embedding"):
            embeddings.append(item.embedding)
        elif isinstance(item, dict):
            embeddings.append(item["embedding"])
    return embeddings


def normalize_embedding(vector: list[float]) -> list[float]:
    """L2-normalize an embedding vector."""
    import math

    magnitude = math.sqrt(sum(v * v for v in vector))
    if magnitude == 0:
        return vector
    return [v / magnitude for v in vector]
