import numpy as np


def cosine_similarity(vec1: list, vec2: list) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec1 (list): First embedding vector.
        vec2 (list): Second embedding vector.

    Returns:
        float: Cosine similarity score between -1 and 1.
    """
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
