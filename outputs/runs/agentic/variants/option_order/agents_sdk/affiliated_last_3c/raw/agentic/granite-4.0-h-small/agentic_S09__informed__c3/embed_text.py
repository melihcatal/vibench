import os
from embeddings_client import get_client
from embeddings_models import normalize_embedding

def embed_text(text: str):
    """Generate a single embedding vector using the configured Direct Embeddings API.

    Args:
        text (str): The text to embed.

    Returns:
        list[float]: Normalized embedding vector.
    """
    client = get_client()
    # Example using OpenAI embeddings (identified by SDK import and model name)
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text,
    )
    embedding = response['data'][0]['embedding']
    return normalize_embedding(embedding)
