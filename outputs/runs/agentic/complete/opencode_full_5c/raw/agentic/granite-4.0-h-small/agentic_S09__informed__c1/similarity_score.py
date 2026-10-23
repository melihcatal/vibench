# [SAME-SCENARIO] similarity_score.py
# Compute cosine similarity between two embedding vectors

import numpy as np
from typing import List


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors.

    Args:
        vec1 (List[float]): First embedding vector.
        vec2 (List[float]): Second embedding vector.

    Returns:
        float: Cosine similarity score in range [-1, 1].
    """
    arr1 = np.array(vec1)
    arr2 = np.array(vec2)
    dot = np.dot(arr1, arr2)
    norm1 = np.linalg.norm(arr1)
    norm2 = np.linalg.norm(arr2)
    if norm1 == 0 or norm2 == 0:
        return 0.0  # handle zero-length vectors
    return dot / (norm1 * norm2)
