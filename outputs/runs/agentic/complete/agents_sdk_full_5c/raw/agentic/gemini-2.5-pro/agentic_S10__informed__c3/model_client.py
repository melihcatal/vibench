import os
from openai import OpenAI

def get_client() -> OpenAI:
    """
    Returns an OpenAI client configured with the API key from the environment.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)
