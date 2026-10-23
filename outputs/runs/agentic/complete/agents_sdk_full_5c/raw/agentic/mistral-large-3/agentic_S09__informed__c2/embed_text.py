import os
from typing import List

from embeddings_client import get_dashscope_client
from embeddings_models import EmbeddingResponse, normalize_embedding


def embed_text(text: str) -> List[float]:
    """Generate embedding vector for a single text string using DashScope."""
    client = get_dashscope_client()
    response = client.call(
        model="text-embedding-v2",
        input=text
    )
    if response.status_code != 200:
        raise RuntimeError(f"DashScope embedding failed: {response.message}")
    
    embedding = response.output["embeddings"][0]["embedding"]
    return normalize_embedding(embedding)