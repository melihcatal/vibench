import os
from typing import List
from embeddings_client import get_cohere_client
from embeddings_models import EmbeddingResponse


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generate embedding vectors for a batch of texts using Cohere Embed API."""
    client = get_cohere_client()
    response = client.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    embedding_response = EmbeddingResponse(response)
    return embedding_response.embeddings