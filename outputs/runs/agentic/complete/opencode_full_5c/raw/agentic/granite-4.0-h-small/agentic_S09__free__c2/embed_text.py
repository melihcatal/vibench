import requests
from embeddings_client import DirectEmbeddingsClient


def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a single text string using the Direct Embeddings API.

    Returns:
        List of floats representing the embedding vector.
    """
    client = DirectEmbeddingsClient()
    resp = client.embed(text=text)
    # Assuming the API returns JSON with a key 'embedding' containing the vector
    return resp["embedding"]
