import os
from typing import List, Dict

from .embeddings_client import get_embedder
from .embeddings_models import normalize_embedding


def embed_text(text: str) -> List[float]:
    """Generate an embedding for a single text string.

    Uses the configured Direct Embeddings provider.
    Returns a list of floats representing the embedding vector.
    """
    client = get_embedder()
    response = client.embed_text(text)
    # Assuming response contains a list/array of floats under 'embedding' key
    embedding = response.get('embedding')
    if embedding is None:
        raise ValueError('Embedding response missing expected field')
    return normalize_embedding(embedding)
