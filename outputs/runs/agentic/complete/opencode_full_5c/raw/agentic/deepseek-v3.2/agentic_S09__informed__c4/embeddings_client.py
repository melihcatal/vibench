import os
import openai
from typing import Optional


def get_embeddings_client(
    api_key: Optional[str] = None, base_url: Optional[str] = None
):
    """Get OpenAI embeddings client with configuration."""
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    return client


def validate_embedding_response(response) -> bool:
    """Validate embedding response structure."""
    if not hasattr(response, "data"):
        return False
    if not isinstance(response.data, list):
        return False
    if len(response.data) == 0:
        return False
    if not hasattr(response.data[0], "embedding"):
        return False
    return True


def get_default_embedding_model() -> str:
    """Get default embedding model."""
    return "text-embedding-3-small"
