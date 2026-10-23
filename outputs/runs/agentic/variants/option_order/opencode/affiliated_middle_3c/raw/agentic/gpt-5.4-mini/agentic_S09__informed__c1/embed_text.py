import os
from embeddings_client import get_embeddings_client, default_embedding_model
from embeddings_models import EmbeddingRequest, extract_embedding_vector


def embed_text(text: str, model: str | None = None):
    client = get_embeddings_client()
    request = EmbeddingRequest(input_texts=[text], model=model or default_embedding_model())
    response = client.embed(request)
    return extract_embedding_vector(response, index=0)
