import os
from dashscope import embeddings  # DashScope Embeddings SDK

# Load API key from environment variable (DashScope uses DASHSCOPE_API_KEY)
API_KEY = os.getenv("DASHSCOPE_API_KEY")


def embed_batch(texts: list[str]):
    """Generate embeddings for a batch of text strings using DashScope.

    Args:
        texts (List[str]): List of input texts.

    Returns:
        List[list[float]]: List of embedding vectors, each as a list of floats.
    """
    # DashScope expects a list of strings
    response = embeddings.embed(texts=texts)
    # Each entry contains an 'embedding' field
    embeddings = [entry["embedding"] for entry in response]
    return embeddings
