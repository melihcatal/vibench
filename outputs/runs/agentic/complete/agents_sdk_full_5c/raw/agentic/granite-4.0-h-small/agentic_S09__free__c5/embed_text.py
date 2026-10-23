import os
from embeddings_client import get_client
from embeddings_models import normalize_embedding

def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a single text string using the Direct Embeddings API.
    """
    client = get_client()
    # Example call to a concrete provider (OpenAI Embeddings)
    response = client.create(
        model="text-embedding-ada-002",
        input=text,
        dimensions=1536,
    )
    # Assume response returns a dict with a key 'embedding' containing a list of floats
    embedding = response.get('embedding', [])
    return normalize_embedding(embedding)
