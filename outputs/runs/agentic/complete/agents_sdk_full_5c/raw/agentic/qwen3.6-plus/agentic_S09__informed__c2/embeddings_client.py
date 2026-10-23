"""
Local helper: Provide configuration and client helper utilities for OpenAI Embeddings API.
Provider: OpenAI Embeddings (openai SDK)
Auth: OPENAI_API_KEY
"""

import os
from typing import Optional

from openai import OpenAI


def get_openai_api_key() -> str:
    """Retrieve the OpenAI API key from environment."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return key


def create_embeddings_client(
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> OpenAI:
    """Create and return a configured OpenAI client for embeddings."""
    resolved_key = api_key or get_openai_api_key()
    kwargs: dict = {"api_key": resolved_key}
    if organization:
        kwargs["organization"] = organization
    if project:
        kwargs["project"] = project
    return OpenAI(**kwargs)


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
