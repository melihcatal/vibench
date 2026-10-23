import os
from embeddings_client import get_embedder


def embed_text(text: str) -> list:
    """Generate an embedding vector for a single text string using the configured provider.

    Args:
        text (str): The input text to embed.

    Returns:
        list: The embedding vector as a list of floats.
    """
    embedder = get_embedder()
    response = embedder.embed_text(text)
    # Assuming response returns a dict with a key 'embedding' containing the vector
    return response["embedding"]
