import os

from embeddings_client import DirectEmbeddingsClient


def embed_text(text: str) -> list:
    client = DirectEmbeddingsClient()
    response = client.embed_text(text)
    return response.embeddings
