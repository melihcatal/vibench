import os
from typing import Optional

import cohere
from cohere import Client
from cohere.core import ApiError


def get_cohere_client() -> Client:
    """Initialize and return a Cohere client using the API key from environment variables."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")
    return cohere.Client(api_key)


def handle_api_error(error: ApiError) -> None:
    """Handle Cohere API errors and raise with context."""
    raise RuntimeError(f"Cohere API error: {error.message}") from error