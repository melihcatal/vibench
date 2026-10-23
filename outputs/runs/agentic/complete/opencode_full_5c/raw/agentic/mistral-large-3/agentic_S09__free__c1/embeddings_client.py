import os
from typing import Optional
from openai import OpenAI


def get_embeddings_client() -> OpenAI:
    """
    Initializes and returns an OpenAI client configured for embeddings.

    Returns:
        Configured OpenAI client instance.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    return OpenAI(api_key=api_key)
