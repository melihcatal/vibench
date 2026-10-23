"""
Local configuration and client helper utilities for Direct Embeddings API.

Provider: OpenAI Embeddings API (https://api.openai.com)
Model: text-embedding-3-small
"""

import os
from typing import Optional, Dict, Any

import openai
from openai import OpenAI


OPENAI_EMBEDDINGS_API_HOST = "api.openai.com"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_EMBEDDING_DIMENSIONS = 1536


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """
    Create and return an OpenAI client configured for embeddings.

    Uses OPENAI_API_KEY environment variable if api_key is not provided.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError(
            "OPENAI_API_KEY environment variable or explicit api_key is required. "
            f"OpenAI embeddings API endpoint: {OPENAI_EMBEDDINGS_API_HOST}"
        )
    client = OpenAI(api_key=key, base_url=f"https://{OPENAI_EMBEDDINGS_API_HOST}/v1")
    return client


def load_embeddings_config() -> Dict[str, Any]:
    """
    Load embeddings configuration from environment variables.

    Returns a dict with model, dimensions, timeout, and retry settings.
    """
    return {
        "model": os.environ.get("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        "dimensions": int(
            os.environ.get("OPENAI_EMBEDDING_DIMENSIONS", DEFAULT_EMBEDDING_DIMENSIONS)
        ),
        "timeout": int(os.environ.get("OPENAI_API_TIMEOUT", "30")),
        "max_retries": int(os.environ.get("OPENAI_MAX_RETRIES", "3")),
    }


def build_embeddings_payload(
    texts: list,
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    encoding_format: str = "float",
) -> Dict[str, Any]:
    """
    Build a normalized payload for OpenAI embeddings API request.

    Args:
        texts: List of text strings to embed
        model: OpenAI embedding model identifier
        dimensions: Optional dimension count for the embedding
        encoding_format: Output format ('float' or 'base64')

    Returns:
        Dict payload ready for OpenAI embeddings.create()
    """
    payload: Dict[str, Any] = {
        "model": model,
        "input": texts,
        "encoding_format": encoding_format,
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload


def parse_embeddings_response(response) -> list:
    """
    Parse OpenAI embeddings API response into a list of embedding vectors.

    Args:
        response: OpenAI API response object from embeddings.create()

    Returns:
        List of embedding vectors (list of floats)
    """
    embeddings = []
    for data_obj in response.data:
        embedding = data_obj.embedding
        embeddings.append(embedding)
    return embeddings
