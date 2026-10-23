import os
from openai import OpenAI


def get_openai_client() -> OpenAI:
    """
    Provides local configuration and client helper utilities for Hosted LLM Inference.
    """
    api_key = os.environ.get("OPENAI_API_KEY")  # Provider-specific environment variable
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)
