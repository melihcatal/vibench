from typing import Optional
import os
from openai import OpenAI


def get_embeddings_client() -> OpenAI:
    """
    Initializes and returns an OpenAI client with API key from environment variables.

    Returns:
        Configured OpenAI client.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    return OpenAI(api_key=api_key)
