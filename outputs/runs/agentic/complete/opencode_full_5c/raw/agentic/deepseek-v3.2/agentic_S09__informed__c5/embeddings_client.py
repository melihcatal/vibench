import os
from typing import Optional
import openai


def get_embeddings_client() -> openai.OpenAI:
    """Provide local configuration and client helper utilities for Direct Embeddings API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    return openai.OpenAI(api_key=api_key, base_url=base_url)


def get_default_model() -> str:
    """Get the default embedding model."""
    return "text-embedding-3-small"


def validate_api_key() -> bool:
    """Validate that the API key is set and appears valid."""
    api_key = os.getenv("OPENAI_API_KEY")
    return bool(api_key and len(api_key) > 20)
