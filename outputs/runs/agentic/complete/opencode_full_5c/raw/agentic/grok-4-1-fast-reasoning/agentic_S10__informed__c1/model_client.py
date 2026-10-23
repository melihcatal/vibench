import os
from mistralai import Mistral


def get_llm_client():
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required")
    return Mistral(api_key=api_key)
