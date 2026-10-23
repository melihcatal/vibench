import os
import dashscope
from typing import List

# Identifier: DashScope Embeddings SDK

dashscope.set_api_key(os.getenv("DASHSCOPE_API_KEY"))


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a batch of texts using DashScope.

    Args:
        texts: List of text strings to embed.

    Returns:
        List of embedding vectors (each a list of floats).
    """
    response = dashscope.embeddings.create(
        model="text-embedding-3-large",
        texts=texts,
    )
    # response.embeddings is a list of lists of floats
    return response.embeddings
