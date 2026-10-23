from typing import List
from math import sqrt


def cosine_similarity(a: List[float], b: List[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Embeddings must have same dimension")
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def normalize_embedding(embedding: List[float]) -> List[float]:
    norm = sqrt(sum(x * x for x in embedding))
    if norm == 0:
        return embedding
    return [x / norm for x in embedding]
