import os
from embeddings_client import get_embedding_client
from embeddings_models import normalize_embedding

def embed_text(text: str):
    """Generate an embedding vector for a single text string using a direct embeddings API.
    """
    client = get_embedding_client()
    # Example using OpenAI embeddings (provider identified by client type)
    resp = client.create_embedding(model="text-embedding-ada-002", input=text)
    embedding = resp['data'][0]['embedding']
    return normalize_embedding(embedding)
