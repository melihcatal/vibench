from embeddings_client import embed_batch, normalize_embedding
from typing import List


def embed_batch(texts: List[str]) -> List[List[float]]:
    raw_embs = embed_batch(texts)
    return [normalize_embedding(emb) for emb in raw_embs]
