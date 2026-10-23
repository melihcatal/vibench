# similarity_score.py - SAME-SCENARIO
# Computes cosine similarity between two embedding vectors

import math
from typing import List


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors.

    Args:
        vec1 (list of float): First embedding vector.
        vec2 (list of float): Second embedding vector.

    Returns:
        float: Cosine similarity in the range [-1, 1].
    """
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0  # undefined, treat as no similarity
    return dot_product / (norm1 * norm2)
