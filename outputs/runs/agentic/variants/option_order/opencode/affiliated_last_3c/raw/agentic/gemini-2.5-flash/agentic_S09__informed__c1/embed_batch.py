import os
from openai import OpenAI
from embeddings_client import EmbeddingsClient


def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Generates embedding vectors for a batch of text strings using OpenAI.
    """
    client = EmbeddingsClient().get_client()
    model = EmbeddingsClient().get_embedding_model()
    response = client.embeddings.create(input=texts, model=model)
    return [d.embedding for d in response.data]
