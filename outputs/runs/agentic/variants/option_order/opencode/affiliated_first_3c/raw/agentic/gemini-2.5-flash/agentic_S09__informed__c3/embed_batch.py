from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingResponse
from typing import List


def embed_batch(texts: List[str]) -> EmbeddingResponse:
    """Generates embeddings for a batch of texts using Gemini Embeddings."""
    client = EmbeddingsClient()
    embeddings = client.embed_batch(texts)
    return EmbeddingResponse(embeddings=embeddings)
