from embeddings_client import EmbeddingsClient
from embeddings_models import normalize_embedding
from typing import List


def embed_batch(texts: List[str]) -> List[List[float]]:
    client = EmbeddingsClient()
    raw_embeddings = client.embed_documents(texts)
    return [normalize_embedding(emb) for emb in raw_embeddings]
