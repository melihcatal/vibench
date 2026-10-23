from typing import List
from embeddings_client import get_cohere_client

# Note: Using a specific model version is a best practice.
COHERE_MODEL_NAME = "embed-english-v3.0"

def embed_batch(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of text strings using Cohere.

    Args:
        texts: A list of text strings to embed.

    Returns:
        A list of embedding vectors.
    """
    client = get_cohere_client()
    response = client.embed(
        texts=texts,
        model=COHERE_MODEL_NAME,
        input_type="search_document"
    )
    return response.embeddings
