import os
from openai import OpenAI

def get_client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    return OpenAI(api_key=key)