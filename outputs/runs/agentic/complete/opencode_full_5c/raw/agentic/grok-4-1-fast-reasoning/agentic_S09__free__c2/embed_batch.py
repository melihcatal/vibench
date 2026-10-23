from typing import List
from embeddings_client import embed_batch
from embeddings_models import l2_normalize


def embed_batch(texts: List[str]) -> List[List[float]]:
    raw_embeddings = embed_batch(model="text-embedding-3-small", texts=texts)
    return [l2_normalize(raw_emb) for raw_emb in raw_embeddings]
