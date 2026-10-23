from typing import List

from embeddings_client import get_dashscope_client
from embeddings_models import EmbeddingResponse, normalize_embedding


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a batch of texts using DashScope."""
    client = get_dashscope_client()
    response = client.call(
        model="text-embedding-v2",
        input=texts
    )
    if response.status_code != 200:
        raise RuntimeError(f"DashScope batch embedding failed: {response.message}")
    
    embeddings = [item["embedding"] for item in response.output["embeddings"]]
    return [normalize_embedding(embedding) for embedding in embeddings]