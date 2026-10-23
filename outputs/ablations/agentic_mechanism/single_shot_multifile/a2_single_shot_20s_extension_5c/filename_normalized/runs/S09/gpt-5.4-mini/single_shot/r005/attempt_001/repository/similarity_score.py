import math
from embed_text import embed_text


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Embedding vectors must have the same length")
    dot = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def similarity_score(text_a: str, text_b: str, model: str | None = None) -> float:
    vec_a = embed_text(text_a, model=model or None)
    vec_b = embed_text(text_b, model=model or None)
    return cosine_similarity(vec_a, vec_b)
