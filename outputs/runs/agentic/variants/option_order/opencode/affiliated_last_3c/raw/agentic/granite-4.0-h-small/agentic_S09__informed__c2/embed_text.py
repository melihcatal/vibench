import dashscope
import os
from embeddings_models import normalize_response

# Provider: DashScope


def embed_text(text: str) -> list:
    """Generate embedding for a single text string using DashScope."""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("Set DASHSCOPE_API_KEY env var")
    client = dashscope.Embeddings(api_key=api_key)
    response = client.embed(text=text)
    return normalize_response(response)[0]
