from typing import List
from embeddings_client import get_embeddings

def embed_batch(texts: List[str]) -> List[List[float]]:
    return get_embeddings(texts, model="text-embedding-3-small")
