import os
from embeddings_client import get_client
from embeddings_models import normalize_embedding, batch_payload

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a batch of texts using the configured Direct Embeddings API.

    Args:
        texts (list[str]): List of texts to embed.

    Returns:
        list[list[float]]: List of normalized embedding vectors.
    """
    client = get_client()
    # OpenAI embeddings identified by SDK and model name
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=texts,
    )
    embeddings = [normalize_embedding(vec) for vec in response['data']]
    return embeddings
