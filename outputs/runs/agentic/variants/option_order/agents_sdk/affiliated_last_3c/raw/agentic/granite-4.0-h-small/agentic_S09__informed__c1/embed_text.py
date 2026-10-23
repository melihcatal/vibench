import os
from embeddings_client import get_embed_client
from embeddings_models import normalize_embedding

def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a single text string.
    Uses the configured Direct Embeddings provider via the helper client.
    """
    client = get_embed_client()
    # The provider SDK is invoked through the client; the concrete provider is identified by the client initialization.
    response = client.embed(text=text)
    # Assuming response contains a field 'embedding' with list of floats
    embedding = response.get('embedding', [])
    return normalize_embedding(embedding)