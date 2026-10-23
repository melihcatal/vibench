import os
import cohere

DEFAULT_MODEL = "embed-english-v3.0"


def get_api_key():
    return os.getenv("COHERE_API_KEY")


def get_embedding_client():
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("COHERE_API_KEY is required")
    return cohere.Client(api_key)

