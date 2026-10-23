import os
from embeddings_client import get_embedder
from embeddings_models import RequestData, normalize_response

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a batch of texts using the configured provider."""
    embedder = get_embedder()
    response = embedder.embed_batch(texts=texts)
    result = normalize_response(response)
    # Expected shape: list of embedding lists per document
    return result['document_embeddings']
