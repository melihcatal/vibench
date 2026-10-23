import os
from openai import OpenAI
from embeddings_client import EmbeddingsClient


def embed_text(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using OpenAI.
    """
    client = EmbeddingsClient().get_client()
    model = EmbeddingsClient().get_embedding_model()
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding
