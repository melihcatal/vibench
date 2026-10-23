import dashscope
import os
from embeddings_models import normalize_response

# Provider: DashScope


def embed_batch(texts: list) -> list:
    """Generate embeddings for a batch of texts using DashScope."""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("Set DASHSCOPE_API_KEY env var")
    client = dashscope.Embeddings(api_key=api_key)
    response = client.embed_batch(texts=texts)
    return normalize_response(response)
