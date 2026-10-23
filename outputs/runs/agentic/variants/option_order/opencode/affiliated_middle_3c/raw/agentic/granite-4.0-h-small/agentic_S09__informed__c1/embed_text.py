import os
from embeddings_client import get_embedder


def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a single text string using the configured provider.

    Args:
        text (str): The text to embed.

    Returns:
        list[float]: The embedding vector.
    """
    client = get_embedder()
    response = client.create_embedding(input=text)
    # Assuming response contains a list of floats under key 'embedding'
    return response["embedding"]
