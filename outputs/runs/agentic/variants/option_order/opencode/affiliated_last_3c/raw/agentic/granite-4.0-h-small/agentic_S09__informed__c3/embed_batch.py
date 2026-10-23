import os
from embeddings_client import get_embedder


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of texts using the configured provider.

    Args:
        texts (list[str]): List of input texts.

    Returns:
        list[list[float]]: List of embedding vectors, one per input text.
    """
    client = get_embedder()
    # Direct Embeddings API expects a list of texts
    embeddings = client.embed_text(texts)
    return embeddings
