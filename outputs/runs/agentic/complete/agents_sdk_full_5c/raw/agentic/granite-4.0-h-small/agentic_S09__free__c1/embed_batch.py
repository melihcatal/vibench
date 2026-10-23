import os
from embeddings_client import DirectEmbeddingsClient
from embeddings_models import normalize_embeddings

client = DirectEmbeddingsClient()

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of text strings."""
    response = client.embed(texts=texts)
    # Assume response contains a list under 'embeddings'
    embeddings = response.get('embeddings')
    if not embeddings:
        raise ValueError('API response missing embeddings')
    return [normalize_embedding(vec) for vec in embeddings]
