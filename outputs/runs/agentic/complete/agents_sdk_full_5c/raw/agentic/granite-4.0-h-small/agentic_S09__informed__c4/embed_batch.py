# embed_batch.py

from embeddings_client import get_client
from embeddings_models import normalize_embedding

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of texts using Direct Embeddings API.

    Args:
        texts (List[str]): List of input texts.

    Returns:
        List[List[float]]: List of normalized embedding vectors.
    """
    client = get_client()
    resp = client.embeddings.create(
        model="text-embedding-ada-002",  # OpenAI model identifier (example)
        input=texts,
    )
    return [normalize_embedding(vec) for vec in resp["data"]["embeddings"]]
