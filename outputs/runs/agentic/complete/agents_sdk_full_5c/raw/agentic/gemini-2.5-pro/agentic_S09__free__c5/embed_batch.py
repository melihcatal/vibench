import os
from typing import List
from embeddings_client import get_embeddings_client

def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of text strings using Google Vertex AI.

    Args:
        texts: A list of texts to embed.

    Returns:
        A list of embedding vectors.
    """
    if not texts or not isinstance(texts, list):
        raise ValueError("Input texts must be a non-empty list of strings.")

    client = get_embeddings_client()
    # The API handles batching under the hood.
    # Model: text-embedding-004
    embeddings = client.get_embeddings(texts)
    
    return [embedding.values for embedding in embeddings]
