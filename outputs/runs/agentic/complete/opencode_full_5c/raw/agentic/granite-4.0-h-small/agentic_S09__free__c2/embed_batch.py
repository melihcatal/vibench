import requests
from embeddings_client import DirectEmbeddingsClient


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of text strings using the Direct Embeddings API.

    Returns:
        List of embedding vectors (each a list of floats).
    """
    client = DirectEmbeddingsClient()
    resp = client.batch_embed(texts=texts)
    # Expected response format: { 'embeddings': [[...], [...], ...] }
    return resp["embeddings"]
