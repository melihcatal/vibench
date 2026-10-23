import os
from math import sqrt
from embeddings_models import normalize_embedding


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    if len(vec1) != len(vec2):
        raise ValueError('Vectors must be of the same dimension')
    norm1 = sqrt(sum(x * x for x in vec1))
    norm2 = sqrt(sum(x * x for x in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return sum(a * b for a, b in zip(vec1, vec2)) / (norm1 * norm2)
