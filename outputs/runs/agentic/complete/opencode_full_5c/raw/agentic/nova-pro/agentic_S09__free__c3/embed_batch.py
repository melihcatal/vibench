import os

from embeddings_client import DirectEmbeddingsClient


def embed_batch(texts: list) -> list:
    client = DirectEmbeddingsClient()
    response = client.embed_batch(texts)
    return response.embeddings
