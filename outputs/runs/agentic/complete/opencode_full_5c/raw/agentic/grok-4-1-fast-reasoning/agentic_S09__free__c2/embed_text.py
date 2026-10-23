from typing import List
from embeddings_client import embed_single
from embeddings_models import l2_normalize


def embed_text(text: str) -> List[float]:
    raw_embedding = embed_single(model="text-embedding-3-small", text=text)
    return l2_normalize(raw_embedding)
