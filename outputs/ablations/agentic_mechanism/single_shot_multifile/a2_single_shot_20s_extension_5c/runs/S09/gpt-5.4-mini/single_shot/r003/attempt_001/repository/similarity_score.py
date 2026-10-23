import math
from typing import Sequence

from embed_text import embed_text


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError("Embedding vectors must have the same length")
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def similarity_score(text_a: str, text_b: str) -> float:
    emb_a = embed_text(text_a)
    emb_b = embed_text(text_b)
    return cosine_similarity(emb_a, emb_b)
