# embed_text.py

from embeddings_client import get_client
from embeddings_models import normalize_embedding

def embed_text(text: str):
    """Generate a single embedding vector for the given text using Direct Embeddings API.

    Args:
        text (str): Input text.

    Returns:
        List[float]: Normalized embedding vector.
    """
    client = get_client()
    resp = client.embeddings.create(
        model="text-embedding-ada-002",  # OpenAI model identifier (example)
        input=text,
    )
    # Expected response: {"data":[{"embedding":[...]}]}
    embedding = resp["data"][0]["embedding"]
    return normalize_embedding(embedding)
