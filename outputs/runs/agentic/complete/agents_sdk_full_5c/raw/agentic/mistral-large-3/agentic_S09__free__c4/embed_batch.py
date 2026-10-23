import os
from typing import List
from embeddings_client import get_embeddings_client

def embed_batch(texts: List[str]) -> List[List[float]]:
    client = get_embeddings_client()
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small"
    )
    return [item.embedding for item in response.data]