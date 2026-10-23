from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingResponse
from typing import List


def embed_text(text: str) -> EmbeddingResponse:
    """Generates an embedding vector for one text string using Gemini Embeddings."""
    client = EmbeddingsClient()
    embedding = client.embed_text(text)
    return EmbeddingResponse(embeddings=[embedding])
