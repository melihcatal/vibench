"""Local configuration and client helper utilities for OpenAI Direct Embeddings API."""

import os
from typing import Optional
from openai import OpenAI

# OpenAI API configuration
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BASE_URL_ENV = "OPENAI_BASE_URL"
OPENAI_DEFAULT_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_ENDPOINT = "https://api.openai.com/v1/embeddings"

# Supported OpenAI embedding models
OPENAI_EMBEDDING_MODELS = {
    "text-embedding-3-small": {
        "dimensions": 1536,
        "max_input_tokens": 8191,
        "description": "Fast, cost-effective embedding model from OpenAI",
    },
    "text-embedding-3-large": {
        "dimensions": 3072,
        "max_input_tokens": 8191,
        "description": "High-dimensional, high-accuracy embedding model from OpenAI",
    },
    "text-embedding-ada-002": {
        "dimensions": 1536,
        "max_input_tokens": 8191,
        "description": "Legacy OpenAI embedding model, still widely used",
    },
}

_client: Optional[OpenAI] = None


def get_openai_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> OpenAI:
    """Get or create a cached OpenAI client instance.

    Uses OPENAI_API_KEY environment variable by default.
    Connects to https://api.openai.com/v1/embeddings endpoint.

    Args:
        api_key: OpenAI API key. If None, reads from OPENAI_API_KEY env var.
        base_url: Optional custom base URL for the API.

    Returns:
        Configured OpenAI client instance.

    Raises:
        ValueError: If no API key is provided or found in environment.
    """
    global _client

    effective_key = api_key or os.environ.get(OPENAI_API_KEY_ENV)
    if not effective_key:
        raise ValueError(
            f"OpenAI API key not found. Set the {OPENAI_API_KEY_ENV} environment variable."
        )

    effective_base_url = base_url or os.environ.get(OPENAI_BASE_URL_ENV)

    if _client is None:
        client_kwargs = {"api_key": effective_key}
        if effective_base_url:
            client_kwargs["base_url"] = effective_base_url
        _client = OpenAI(**client_kwargs)
    elif api_key is not None or base_url is not None:
        client_kwargs = {"api_key": effective_key}
        if effective_base_url:
            client_kwargs["base_url"] = effective_base_url
        _client = OpenAI(**client_kwargs)

    return _client


def reset_client():
    """Reset the cached client to force re-creation."""
    global _client
    _client = None


def get_model_info(model: str) -> dict:
    """Get information about an OpenAI embedding model."""
    return OPENAI_EMBEDDING_MODELS.get(
        model,
        {"dimensions": None, "max_input_tokens": None, "description": "Unknown model"},
    )


def get_supported_models() -> list[str]:
    """Return list of supported OpenAI embedding model identifiers."""
    return list(OPENAI_EMBEDDING_MODELS.keys())


def validate_model(model: str) -> bool:
    """Check if a model identifier is supported."""
    return model in OPENAI_EMBEDDING_MODELS


def get_api_endpoint() -> str:
    """Return the OpenAI embeddings API endpoint URL."""
    return OPENAI_EMBEDDING_ENDPOINT
