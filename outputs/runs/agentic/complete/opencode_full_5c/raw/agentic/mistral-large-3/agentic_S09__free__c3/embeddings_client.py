import os
from typing import Optional
from openai import OpenAI


def get_embeddings_client() -> OpenAI:
    """
    Initializes and returns an OpenAI client configured for embeddings.

    Returns:
        OpenAI: Configured OpenAI client instance.

    Raises:
        ValueError: If the OPENAI_API_KEY environment variable is not set.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    return OpenAI(api_key=api_key)
