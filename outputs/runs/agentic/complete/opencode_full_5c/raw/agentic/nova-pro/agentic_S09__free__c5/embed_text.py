import os

from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()


def generate_embedding(text: str) -> list[float]:
    response = client.generate_embedding(text)
    return response["embedding"]
