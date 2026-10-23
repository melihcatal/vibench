import os
from openai import OpenAI

def get_client() -> OpenAI:
    """Provide a configured OpenAI client for Direct Embeddings API.

    The client uses environment variable OPENAI_API_KEY for authentication.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)
