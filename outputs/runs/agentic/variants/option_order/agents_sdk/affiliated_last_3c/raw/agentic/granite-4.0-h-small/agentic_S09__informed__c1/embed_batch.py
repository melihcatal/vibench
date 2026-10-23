import os
from embeddings_client import get_embed_client
from embeddings_models import normalize_embedding_batch

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a list of texts.
    Uses the configured Direct Embeddings provider via the helper client.
    """
    client = get_embed_client()
    response = client.embed_batch(texts=texts)
    # Expected response format: list of dicts each containing 'embedding'
    embeddings = [item.get('embedding', []) for item in response]
    return [normalize_embedding(e) for e in embeddings]
