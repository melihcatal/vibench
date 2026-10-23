from typing import List
from .embeddings_client import EmbeddingsClient
from .embeddings_models import normalize_embedding


def embed_batch(texts: List[str], dimensions: int = None) -> List[List[float]]:
    """Generate embeddings for a batch of texts using OpenAI's text-embedding-3-small model."""
    client = EmbeddingsClient()
    response = client.embed(texts, dimensions=dimensions)
    return [normalize_embedding(embedding) for embedding in response.embeddings]
