import os
from typing import List
from embeddings_client import get_embeddings_client
from embeddings_models import EmbeddingRequest, normalize_text


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """Generate embeddings for a batch of texts."""
    client = get_embeddings_client()

    normalized_texts = [normalize_text(text) for text in texts]

    response = client.embeddings.create(model=model, input=normalized_texts)

    return [item.embedding for item in response.data]
