import os
from openai import OpenAI

def get_model_client() -> OpenAI:
    """
    Returns a configured OpenAI client.
    Expects the OPENAI_API_KEY environment variable to be set.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = OpenAI(api_key=api_key)
    return client
