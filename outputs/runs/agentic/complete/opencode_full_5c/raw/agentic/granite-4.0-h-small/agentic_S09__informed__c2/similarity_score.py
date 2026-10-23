import numpy as np


def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec1 (List[float]): First embedding.
        vec2 (List[float]): Second embedding.

    Returns:
        float: Cosine similarity in range [-1, 1].
    """
    arr1 = np.array(vec1)
    arr2 = np.array(vec2)
    dot_product = np.dot(arr1, arr2)
    norm1 = np.linalg.norm(arr1)
    norm2 = np.linalg.norm(arr2)
    if norm1 == 0 or norm2 == 0:
        return 0.0  # undefined similarity -> treat as 0
    return dot_product / (norm1 * norm2)
