import os
from embeddings_client import create_client
from embeddings_models import normalize_embedding

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a batch of text strings using OpenAI Embeddings.
    Returns a list of normalized embedding vectors (each as list of floats).
    """
    client = create_client()
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=texts,
    )
    return [normalize_embedding(vec) for vec in response.data]