import os
from openai import OpenAI

def get_openai_client() -> OpenAI:
    """
    Provides a configured OpenAI client.
    """
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    )

def get_default_model() -> str:
    """
    Returns the default OpenAI model identifier.
    """
    return os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o")