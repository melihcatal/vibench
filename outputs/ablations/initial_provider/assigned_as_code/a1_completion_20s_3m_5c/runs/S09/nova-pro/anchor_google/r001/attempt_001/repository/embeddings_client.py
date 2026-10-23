import os
from google import genai


def get_embeddings_client(config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["GOOGLE_API_KEY"]
    return genai.Client(api_key=api_key)