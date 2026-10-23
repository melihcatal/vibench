import os

from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    response = client.generate_embeddings(texts)
    return response["embeddings"]
