"""
Local configuration and client helper utilities for Direct Embeddings API.
Uses OpenAI API (api.openai.com) for embedding generation.
"""

import os
from typing import List, Optional, Dict, Any

from openai import OpenAI
from openai._types import NOT_GIVEN


# Provider-specific configuration
OPENAI_EMBEDDING_API_HOST = "api.openai.com"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
LARGE_EMBEDDING_MODEL = "text-embedding-3-large"
DEFAULT_DIMENSIONS = 1536


def get_openai_client(
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    timeout: float = 60.0,
) -> OpenAI:
    """Create an OpenAI client using provider-specific environment variables."""
    resolved_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    resolved_org = organization or os.environ.get("OPENAI_ORG_ID")

    client_kwargs: Dict[str, Any] = {
        "api_key": resolved_key,
        "timeout": timeout,
        "base_url": f"https://{OPENAI_EMBEDDING_API_HOST}/v1",
    }

    if resolved_org:
        client_kwargs["organization"] = resolved_org

    return OpenAI(**client_kwargs)


def resolve_model(
    model_name: Optional[str] = None,
    prefer_large: bool = False,
) -> str:
    """Resolve the OpenAI embedding model identifier."""
    if model_name:
        return model_name
    if prefer_large:
        return LARGE_EMBEDDING_MODEL
    return DEFAULT_EMBEDDING_MODEL


def build_embedding_payload(
    input_text: str,
    model: str,
    dimensions: Optional[int] = None,
    encoding_format: str = "float",
) -> Dict[str, Any]:
    """Build a normalized payload for OpenAI embeddings.create()."""
    payload: Dict[str, Any] = {
        "model": model,
        "input": input_text,
        "encoding_format": encoding_format,
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload


def build_batch_embedding_payload(
    texts: List[str],
    model: str,
    dimensions: Optional[int] = None,
    encoding_format: str = "float",
) -> Dict[str, Any]:
    """Build a normalized payload for batch OpenAI embeddings.create()."""
    payload: Dict[str, Any] = {
        "model": model,
        "input": texts,
        "encoding_format": encoding_format,
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions
    return payload


def extract_embedding_vector(response_data: Any) -> List[float]:
    """Extract the raw embedding vector from an OpenAI API response."""
    if hasattr(response_data, "data"):
        return response_data.data[0].embedding
    if isinstance(response_data, dict):
        return response_data["data"][0]["embedding"]
    raise ValueError("Unexpected response format from OpenAI embeddings API")


def extract_batch_embeddings(response_data: Any) -> List[List[float]]:
    """Extract all embedding vectors from a batch OpenAI API response."""
    if hasattr(response_data, "data"):
        return [item.embedding for item in response_data.data]
    if isinstance(response_data, dict):
        return [item["embedding"] for item in response_data["data"]]
    raise ValueError("Unexpected response format from OpenAI embeddings API")


def get_token_usage(response_data: Any) -> int:
    """Extract token usage from OpenAI API response."""
    if hasattr(response_data, "usage"):
        return response_data.usage.total_tokens
    if isinstance(response_data, dict):
        return response_data.get("usage", {}).get("total_tokens", 0)
    return 0
