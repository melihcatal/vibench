import os
from openai import OpenAI
from embeddings_client import EmbeddingsClient


def embed_query(query: str) -> list[float]:
    """
    Embeds a query string for semantic search using OpenAI.
    """
    client = EmbeddingsClient().get_client()
    model = EmbeddingsClient().get_embedding_model()
    response = client.embeddings.create(input=query, model=model)
    return response.data[0].embedding


def embed_documents(documents: list[str]) -> list[list[float]]:
    """
    Embeds a list of document strings for semantic search using OpenAI.
    """
    client = EmbeddingsClient().get_client()
    model = EmbeddingsClient().get_embedding_model()
    response = client.embeddings.create(input=documents, model=model)
    return [d.embedding for d in response.data]
