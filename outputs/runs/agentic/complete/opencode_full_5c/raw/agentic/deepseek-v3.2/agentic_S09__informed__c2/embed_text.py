import os
from typing import List
from embeddings_client import get_embeddings_client


def embed_text(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Generate an embedding vector for a single text string using OpenAI Embeddings.

    Args:
        text: The text string to embed
        model: The OpenAI embedding model identifier

    Returns:
        List[float]: The embedding vector
    """
    client = get_embeddings_client()

    response = client.embeddings.create(model=model, input=text)

    return response.data[0].embedding
