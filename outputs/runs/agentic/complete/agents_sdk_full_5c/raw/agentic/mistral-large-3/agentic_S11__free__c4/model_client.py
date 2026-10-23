import os
from openai import OpenAI

def get_model_client() -> OpenAI:
    """
    Returns an OpenAI client configured via environment variables.
    Requires OPENAI_API_KEY and optionally OPENAI_BASE_URL.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    return OpenAI(api_key=api_key, base_url=base_url)