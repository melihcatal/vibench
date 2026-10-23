import os
from embeddings_client import DirectEmbeddingsClient
from embeddings_models import normalize_embedding

client = DirectEmbeddingsClient()

def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a single text string."""
    response = client.embed(text=text)
    # Assume API returns a JSON with a field 'embedding' as list of floats
    embedding = response.get('embedding')
    if not embedding:
        raise ValueError('API response missing embedding')
    return normalize_embedding(embedding)
