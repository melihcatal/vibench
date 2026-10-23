# embed_batch.py - SAME-SCENARIO
# Generates embeddings for a batch of text strings using DashScope Embeddings

import os
import dashscope

# Load API key from environment
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise ValueError("Set DASHSCOPE_API_KEY environment variable")

dashscope.api_key = DASHSCOPE_API_KEY


def embed_batch(texts: list) -> list:
    """Return a list of embedding vectors (each a list of floats) for the given texts.

    Args:
        texts (list): List of strings to embed.

    Returns:
        list: List of embedding vectors corresponding to each input text.
    """
    response = dashscope.embeddings.create(
        model="text-embedding-003",  # concrete model identifier
        texts=texts,
    )
    # Each element in response['embeddings'] contains the vector list
    return [emb["data"] for emb in response["embeddings"]]
