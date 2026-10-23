from embeddings_client import embed_single, normalize_embedding
from typing import List


def embed_text(text: str) -> List[float]:
    raw_emb = embed_single(text)
    return normalize_embedding(raw_emb)
