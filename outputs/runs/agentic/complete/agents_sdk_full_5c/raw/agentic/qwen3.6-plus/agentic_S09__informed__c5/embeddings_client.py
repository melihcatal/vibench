"""
Local helper: Provide configuration and client helper utilities for Direct Embeddings API.
Provider: OpenAI Embeddings API (text-embedding-3-small)
"""

import os
from typing import Optional

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_HOST = "api.openai.com"


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Create an OpenAI client for embeddings, reading from OPENAI_API_KEY env var."""
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for OpenAI embeddings."
        )
    return OpenAI(api_key=key)


def validate_api_key(api_key: Optional[str] = None) -> bool:
    """Check whether an OpenAI API key is available."""
    key = api_key or os.environ.get("OPENAI_API_KEY")
    return key is not None and len(key.strip()) > 0


def get_embedding_model() -> str:
    """Return the concrete OpenAI embedding model identifier."""
    return OPENAI_EMBEDDING_MODEL


def build_client_kwargs(
    api_key: Optional[str] = None,
    timeout: int = 30,
    max_retries: int = 3,
) -> dict:
    """Build keyword arguments for the OpenAI client constructor."""
    key = api_key or os.environ.get("OPENAI_API_KEY")
    return {
        "api_key": key,
        "timeout": timeout,
        "max_retries": max_retries,
    }
