import os
from embeddings_client import get_embeddings_client, default_embedding_model
from embeddings_models import EmbeddingRequest, extract_embeddings_vectors


def embed_batch(texts: list[str], model: str | None = None):
    client = get_embeddings_client()
    request = EmbeddingRequest(input_texts=texts, model=model or default_embedding_model())
    response = client.embed(request)
    return extract_embeddings_vectors(response)
