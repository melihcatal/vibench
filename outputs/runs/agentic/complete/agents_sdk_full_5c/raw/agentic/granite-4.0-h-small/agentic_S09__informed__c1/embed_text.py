import os
from embeddings_client import create_client
from embeddings_models import normalize_embedding

def embed_text(text: str) -> list[float]:
    """Generate embedding vector for a single text string using OpenAI Embeddings.
    Returns a normalized list of floats.
    """
    client = create_client()
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text,
    )
    embedding = response.data[0].embedding
    return normalize_embedding(embedding)