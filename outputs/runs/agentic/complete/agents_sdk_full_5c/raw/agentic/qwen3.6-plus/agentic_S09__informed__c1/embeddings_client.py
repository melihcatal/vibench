"""Local configuration and client helper utilities for Direct Embeddings API.

Provides an OpenAI embeddings client wrapper with environment-based configuration.
"""

import os
from typing import List, Optional

from openai import OpenAI


def get_openai_client() -> OpenAI:
    """Create and return an OpenAI client configured from environment variables."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def get_embedding_model() -> str:
    """Return the configured OpenAI embedding model identifier."""
    return os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def create_embedding(
    client: OpenAI,
    text: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[float]:
    """Create a single embedding using OpenAI's embeddings API.

    Args:
        client: OpenAI client instance.
        text: Input text to embed.
        model: OpenAI embedding model ID (defaults to configured model).
        dimensions: Optional output dimensionality for the embedding.

    Returns:
        List of floats representing the embedding vector.
    """
    model_id = model or get_embedding_model()
    params: dict = {
        "input": text,
        "model": model_id,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)
    return response.data[0].embedding


def create_batch_embeddings(
    client: OpenAI,
    texts: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """Create embeddings for a batch of texts using OpenAI's embeddings API.

    Args:
        client: OpenAI client instance.
        texts: List of input texts to embed.
        model: OpenAI embedding model ID (defaults to configured model).
        dimensions: Optional output dimensionality for each embedding.

    Returns:
        List of embedding vectors, one per input text.
    """
    model_id = model or get_embedding_model()
    params: dict = {
        "input": texts,
        "model": model_id,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)
    return [item.embedding for item in response.data]
