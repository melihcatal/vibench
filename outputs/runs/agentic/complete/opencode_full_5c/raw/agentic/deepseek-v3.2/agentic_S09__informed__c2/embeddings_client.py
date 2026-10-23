import os
from typing import Optional
from openai import OpenAI


def get_embeddings_client() -> OpenAI:
    """
    Get OpenAI client for embeddings API.

    Returns:
        OpenAI: Configured OpenAI client

    Raises:
        ValueError: If OPENAI_API_KEY is not set
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    base_url = os.getenv("OPENAI_BASE_URL")

    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url

    return OpenAI(**client_kwargs)


def normalize_embedding(embedding: list) -> list:
    """
    Normalize embedding vector to unit length.

    Args:
        embedding: Raw embedding vector

    Returns:
        list: Normalized embedding vector
    """
    import numpy as np

    vec = np.array(embedding)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()


def validate_text_length(text: str, max_length: int = 8192) -> bool:
    """
    Validate text length for embedding API.

    Args:
        text: Text to validate
        max_length: Maximum allowed length

    Returns:
        bool: True if text is within length limit
    """
    return len(text) <= max_length


def truncate_text(text: str, max_length: int = 8192) -> str:
    """
    Truncate text to maximum length for embedding API.

    Args:
        text: Text to truncate
        max_length: Maximum allowed length

    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length]
