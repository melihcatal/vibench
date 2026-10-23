from typing import List
from embeddings_client import embed_single
from embeddings_models import l2_normalize, cosine_similarity


def similarity_score(text1: str, text2: str) -> float:
    emb1 = l2_normalize(embed_single(model="text-embedding-3-small", text=text1))
    emb2 = l2_normalize(embed_single(model="text-embedding-3-small", text=text2))
    return cosine_similarity(emb1, emb2)
