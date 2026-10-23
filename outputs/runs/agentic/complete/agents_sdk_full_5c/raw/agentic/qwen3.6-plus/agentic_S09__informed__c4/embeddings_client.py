"""
Local configuration and client helper utilities for OpenAI Embeddings API.

Provides a configured OpenAI embeddings client and shared utilities
for embedding requests using the openai SDK.
"""

import os
from typing import Optional

import openai


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIMENSIONS = 1536
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def get_openai_client(api_key: Optional[str] = None) -> openai.OpenAI:
    """
    Create and return an authenticated OpenAI client for embeddings.

    Args:
        api_key: Optional API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Configured openai.OpenAI instance.
    """
    key = api_key or os.environ.get(OPENAI_API_KEY_ENV)
    if not key:
        raise ValueError(
            f"OpenAI API key not provided and {OPENAI_API_KEY_ENV} not set"
        )
    return openai.OpenAI(api_key=key)


def get_embeddings_client(
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: int = OPENAI_EMBEDDING_DIMENSIONS,
) -> openai.OpenAI:
    """
    Return an OpenAI client pre-configured for embedding operations.

    Args:
        api_key: OpenAI API key.
        model: Model identifier, default text-embedding-3-small.
        dimensions: Output vector dimensions, default 1536.

    Returns:
        openai.OpenAI client instance.
    """
    return get_openai_client(api_key)


def normalize_input_text(text: str) -> str:
    """
    Normalize input text for embedding.

    Strips excess whitespace and ensures non-empty input.
    """
    cleaned = " ".join(text.split())
    if not cleaned:
        raise ValueError("Input text is empty after normalization")
    return cleaned


def build_embedding_payload(
    input_text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = OPENAI_EMBEDDING_DIMENSIONS,
) -> dict:
    """
    Build a normalized payload dict for OpenAI embeddings.create().

    Args:
        input_text: Raw text to embed.
        model: OpenAI embedding model ID.
        dimensions: Optional output dimensions.

    Returns:
        Dict suitable for openai_client.embeddings.create(**payload).
    """
    cleaned = normalize_input_text(input_text)
    payload = {"model": model, "input": cleaned}
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload
