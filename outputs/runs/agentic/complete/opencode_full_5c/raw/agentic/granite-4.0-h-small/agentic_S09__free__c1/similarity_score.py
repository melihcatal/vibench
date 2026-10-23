# [SAME-SCENARIO] similarity_score.py
# Computes cosine similarity between two embedding vectors

import math
from typing import List


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Return cosine similarity between two vectors.

    Both vectors must be of equal length.
    """
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must be the same length")
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)
