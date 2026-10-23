import os
from embeddings_client import get_embedder


def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a single text string using the configured provider.

    Args:
        text (str): The input text to embed.

    Returns:
        list[float]: The embedding vector.
    """
    client = get_embedder()
    # Direct Embeddings API expects a list of texts
    embeddings = client.embed_text([text])
    # Assuming the API returns a list of embedding arrays per input text
    return embeddings[0]
