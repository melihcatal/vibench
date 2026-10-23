"""
Local configuration and client helper utilities for Direct Embeddings API.
Uses OpenAI embeddings API (api.openai.com) as the concrete provider.
"""

import os
from typing import Optional

from openai import OpenAI


def get_openai_client(api_key: Optional[str] = None, timeout: float = 30.0) -> OpenAI:
    """
    Create and return an OpenAI client configured with the provided or
    environment-sourced API key targeting api.openai.com.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError(
            "OPENAI_API_KEY environment variable or api_key parameter is required"
        )
    return OpenAI(
        api_key=key,
        timeout=timeout,
    )


def get_default_model() -> str:
    """Return the default OpenAI embedding model identifier."""
    return os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def configure_client(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    timeout: float = 30.0,
) -> tuple[OpenAI, str]:
    """
    Configure and return an OpenAI client along with the model identifier.
    Returns (client, model_name).
    """
    client = get_openai_client(api_key=api_key, timeout=timeout)
    model_name = model or get_default_model()
    return client, model_name
