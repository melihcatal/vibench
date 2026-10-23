import os
from google import genai

def get_embeddings_client(api_key: str = None):
    """Initializes and returns a Google Generative AI client for embeddings."""
    api_key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API Key not found. Please set GOOGLE_API_KEY environment variable or pass it directly.")
    return genai.Client(api_key=api_key)
