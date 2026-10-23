import os
import cohere
from typing import Optional


def get_cohere_client() -> cohere.Client:
    """Initialize and return a Cohere client using the API key from environment variables."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return cohere.Client(api_key)