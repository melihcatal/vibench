# embed_text.py
import os
from embeddings_client import DirectEmbeddingsClient
from embeddings_models import normalize_embedding

def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a single text string using the Direct Embeddings API.",
    client = DirectEmbeddingsClient()
    response = client.embed(text=text)
    # Assume response is a dict with a key "embedding" containing a list of floats
    return normalize_embedding(response["embedding"]) 