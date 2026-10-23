import numpy as np


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec1 (list[float]): First embedding vector.
        vec2 (list[float]): Second embedding vector.

    Returns:
        float: Cosine similarity score in range [-1, 1].
    """
    arr1 = np.array(vec1, dtype=np.float32)
    arr2 = np.array(vec2, dtype=np.float32)
    dot_product = np.dot(arr1, arr2)
    norm1 = np.linalg.norm(arr1)
    norm2 = np.linalg.norm(arr2)
    if norm1 == 0 or norm2 == 0:
        return 0.0  # undefined similarity, treat as 0
    return dot_product / (norm1 * norm2)
