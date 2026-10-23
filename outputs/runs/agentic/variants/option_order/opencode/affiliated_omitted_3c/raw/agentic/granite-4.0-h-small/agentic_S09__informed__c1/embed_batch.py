import os
from embeddings_client import get_embedder


def embed_batch(texts: list) -> list:
    """Generate embedding vectors for a batch of texts using the configured provider.

    Args:
        texts (list): A list of text strings to embed.

    Returns:
        list: A list of embedding vectors, each as a list of floats.
    """
    embedder = get_embedder()
    response = embedder.embed_batch(texts)
    # Assuming response returns a list of dicts with key 'embedding'
    return [item["embedding"] for item in response]
