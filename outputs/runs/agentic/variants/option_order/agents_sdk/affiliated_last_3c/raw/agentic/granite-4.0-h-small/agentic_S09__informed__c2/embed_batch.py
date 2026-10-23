import os
from embeddings_client import DirectEmbeddingsClient
from embeddings_models import normalize_embedding


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a batch of text strings.

    Args:
        texts (list[str]): List of texts to embed.

    Returns:
        list[list[float]]: List of embedding vectors, one per input text.
    """
    client = DirectEmbeddingsClient()
    response = client.embed_batch(texts=texts)
    # Assume response shape: {'embeddings': [[float,...], ...]}
    embeddings = response.get('embeddings')
    if embeddings is None:
        raise ValueError('Embedding batch response missing expected "embeddings" field')
    # Normalize each vector
    return [normalize_embedding(vec) for vec in embeddings]
