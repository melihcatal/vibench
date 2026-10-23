import os
from embeddings_client import get_embedder


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of text strings using the configured provider.

    Args:
        texts (list[str]): List of texts to embed.

    Returns:
        list[list[float]]: List of embedding vectors corresponding to each input text.
    """
    client = get_embedder()
    response = client.create_embedding_batch(input=texts)
    # Assuming response contains a list of embedding lists under key 'embeddings'
    return response["embeddings"]
