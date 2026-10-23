# embed_text.py
# SAME-SCENARIO
from embeddings_client import get_embed_client
from embeddings_models import normalize_embedding

def embed_text(text: str):
    """Generate a single embedding vector for the given text string.

    Uses the configured Direct Embeddings provider (e.g., OpenAI).
    Returns a normalized numpy array embedding.
    """
    client = get_embed_client()
    response = client.create(content=text, model="text-embedding-ada-002")
    embedding = response['data'][0]['embedding']
    return normalize_embedding(embedding)
