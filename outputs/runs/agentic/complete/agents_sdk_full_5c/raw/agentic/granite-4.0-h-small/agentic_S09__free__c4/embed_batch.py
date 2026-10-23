# embed_batch.py
import os
from embeddings_client import DirectEmbeddingsClient
from embeddings_models import normalize_embedding

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of text strings using the Direct Embeddings API.",
    client = DirectEmbeddingsClient()
    response = client.embed_batch(texts=texts)
    # Assume response is a dict with a key "embeddings" containing a list of embedding lists
    return [normalize_embedding(vec) for vec in response["embeddings"]]