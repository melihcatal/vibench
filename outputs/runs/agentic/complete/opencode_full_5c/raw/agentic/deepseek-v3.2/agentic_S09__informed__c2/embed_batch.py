import os
from typing import List, Dict, Any
from embeddings_client import get_embeddings_client


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """
    Generate embeddings for a batch of texts using OpenAI Embeddings.

    Args:
        texts: List of text strings to embed
        model: The OpenAI embedding model identifier

    Returns:
        List[List[float]]: List of embedding vectors
    """
    client = get_embeddings_client()

    response = client.embeddings.create(model=model, input=texts)

    return [item.embedding for item in response.data]
