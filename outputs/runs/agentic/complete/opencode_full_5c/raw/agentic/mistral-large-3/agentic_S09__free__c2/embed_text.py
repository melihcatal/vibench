import numpy as np
from typing import List
from .embeddings_client import EmbeddingsClient
from .embeddings_models import normalize_embedding


def embed_text(text: str, dimensions: int = None) -> List[float]:
    """Generate an embedding vector for a single text string using OpenAI's text-embedding-3-small model."""
    client = EmbeddingsClient()
    response = client.embed([text], dimensions=dimensions)
    embedding = response.embeddings[0]
    return normalize_embedding(embedding)
