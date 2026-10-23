import os
from openai import OpenAI

def get_model_client():
    """
    Initializes and returns the OpenAI client.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = OpenAI(api_key=api_key)
    return client
