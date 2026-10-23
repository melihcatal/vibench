import os
from embeddings_client import get_embeddings_client

def generate_text_embedding(text: str) -> list[float]:
    """
    Generates an embedding for a single text string using Google Vertex AI.

    Args:
        text: The text to embed.

    Returns:
        The embedding vector.
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string.")

    client = get_embeddings_client()
    embeddings = client.get_embeddings([text])
    
    return embeddings[0].values
