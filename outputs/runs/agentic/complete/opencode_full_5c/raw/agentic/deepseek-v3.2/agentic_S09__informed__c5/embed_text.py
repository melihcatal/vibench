import os
from embeddings_client import get_embeddings_client
from embeddings_models import EmbeddingRequest, normalize_text


def embed_text(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """Generate an embedding vector for one text string."""
    client = get_embeddings_client()

    normalized_text = normalize_text(text)

    response = client.embeddings.create(model=model, input=normalized_text)

    return response.data[0].embedding
