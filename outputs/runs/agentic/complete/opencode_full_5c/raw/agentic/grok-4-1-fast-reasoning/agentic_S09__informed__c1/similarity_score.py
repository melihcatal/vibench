from embed_text import embed_text
from embeddings_models import cosine_similarity
from typing import List


def similarity_score(text1: str, text2: str) -> float:
    emb1 = embed_text(text1)
    emb2 = embed_text(text2)
    return cosine_similarity(emb1, emb2)
