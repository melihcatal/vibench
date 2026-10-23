import os
from openai import OpenAI

def get_openai_client():
    """
    Initializes and returns an OpenAI client.
    Requires OPENAI_API_KEY environment variable to be set.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)
