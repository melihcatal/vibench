import os
from dashscope import embeddings  # DashScope Embeddings SDK

# Load API key from environment variable (DashScope uses DASHSCOPE_API_KEY)
API_KEY = os.getenv("DASHSCOPE_API_KEY")


def embed_text(text: str):
    """Generate an embedding vector for a single text string using DashScope.

    Args:
        text (str): The input text to embed.

    Returns:
        list[float]: Embedding vector as a list of floats.
    """
    # DashScope expects a list of strings
    response = embeddings.embed(texts=[text])
    # DashScope returns a list of dicts with 'embedding' key
    embedding = response[0]["embedding"]
    return embedding
