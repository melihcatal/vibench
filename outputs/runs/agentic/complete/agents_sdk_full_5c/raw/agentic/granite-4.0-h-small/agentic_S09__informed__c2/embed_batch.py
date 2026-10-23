import os
from typing import List, Dict

from .embeddings_client import get_embedder
from .embeddings_models import normalize_embedding


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a batch of text strings.

    Uses the configured Direct Embeddings provider.
    Returns a list of embedding vectors, one per input text.
    """
    client = get_embedder()
    response = client.embed_batch(texts)
    # Assuming response returns a list of embeddings under 'embeddings' key
    embeddings = response.get('embeddings')
    if embeddings is None:
        raise ValueError('Batch response missing expected field')
    return [normalize_embedding(e) for e in embeddings]
