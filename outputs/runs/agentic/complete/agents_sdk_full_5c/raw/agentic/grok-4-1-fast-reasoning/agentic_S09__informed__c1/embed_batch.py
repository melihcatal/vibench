from typing import List
from embeddings_client import EmbeddingsClient

def embed_batch(texts: List[str]) -> List[List[float]]:
    client = EmbeddingsClient()
    return client.embed_texts(texts)
