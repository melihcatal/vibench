import os
from openai import OpenAI

def get_openai_client(api_key: str = None):
    """
    Returns an OpenAI client instance.
    API key can be provided directly or will be read from OPENAI_API_KEY environment variable.
    """
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not provided and not found in environment variables.")
    return OpenAI(api_key=api_key)
