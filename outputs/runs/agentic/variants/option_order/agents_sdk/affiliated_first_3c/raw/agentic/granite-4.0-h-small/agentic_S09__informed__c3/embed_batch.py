import os
from embeddings_client import get_embed_client
from embeddings_models import normalize_embedding

def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a single text string.
    
    Uses the configured provider (e.g., OpenAI) and returns a normalized list of floats.
    """
    client = get_embed_client()
    response = client.embed(text=text)
    # Assumes response['embedding'] is a list of numbers
    return normalize_embedding(response['embedding'])