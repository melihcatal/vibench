"""
Embed model outputs for clustering or retrieval.

Provider: OpenAI Embeddings API
SDK: openai
Auth: OPENAI_API_KEY
Concrete model: text-embedding-3-small, text-embedding-3-large
Endpoint: api.openai.com/v1/embeddings
"""

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _resolve_openai_config() -> Dict[str, str]:
    """Resolve OpenAI configuration from environment variables."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is required for OpenAI Embeddings integration"
        )
    base_url = os.environ.get("OPENAI_BASE_URL")
    config: Dict[str, str] = {"api_key": api_key}
    if base_url:
        config["base_url"] = base_url
    return config


def create_openai_client() -> OpenAI:
    """Create and return a configured OpenAI client instance."""
    config = _resolve_openai_config()
    return OpenAI(**config)


def embed_text(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> List[float]:
    """
    Generate an embedding vector for a single text using OpenAI.

    Provider: OpenAI Embeddings API
    Models: text-embedding-3-small, text-embedding-3-large
    Endpoint: api.openai.com/v1/embeddings

    Args:
        text: The text to embed.
        model: OpenAI embedding model identifier.
               Defaults to 'text-embedding-3-small'.
        dimensions: Optional output dimensionality reduction.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = create_openai_client()

    kwargs: Dict[str, Any] = {
        "model": model,
        "input": text,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)
    return response.data[0].embedding


def embed_batch(
    texts: List[str],
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """
    Generate embeddings for multiple texts using OpenAI.

    Provider: OpenAI Embeddings API

    Args:
        texts: List of texts to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality.

    Returns:
        List of embedding vectors, one per input text.
    """
    client = create_openai_client()

    kwargs: Dict[str, Any] = {
        "model": model,
        "input": texts,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)
    return [item.embedding for item in response.data]


def embed_model_output(
    output_text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = 256,
) -> Dict[str, Any]:
    """
    Embed a model's generated output for downstream clustering or retrieval.

    Args:
        output_text: The text output from a hosted LLM.
        model: OpenAI embedding model (e.g., text-embedding-3-small).
        dimensions: Target embedding dimensionality.

    Returns:
        Dictionary containing the embedding vector and metadata.
    """
    embedding = embed_text(
        text=output_text,
        model=model,
        dimensions=dimensions,
    )
    return {
        "text": output_text[:100] + ("..." if len(output_text) > 100 else ""),
        "full_text": output_text,
        "embedding": embedding,
        "dimensionality": len(embedding),
        "model": model,
        "provider": "openai",
    }
