import numpy as np


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.
    Returns a float between -1 and 1.
    """
    arr1, arr2 = np.array(vec1), np.array(vec2)
    norm1, norm2 = np.linalg.norm(arr1), np.linalg.norm(arr2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(arr1, arr2) / (norm1 * norm2))
