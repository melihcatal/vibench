import os

from google import genai


def get_embeddings_client(api_key=None):
    api_key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found. Please set GOOGLE_API_KEY environment variable or pass it directly.")
    return genai.Client(api_key=api_key)

def get_embedding_model_name():
    return "gemini-embedding-001"
