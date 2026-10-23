# similarity_score.py
# [SAME-SCENARIO] Computes cosine similarity between two embedded texts

import numpy as np


def cosine_similarity(embedding_a: list[float], embedding_b: list[float]) -> float:
    """Calculate cosine similarity between two embedding vectors.
    Args:
        embedding_a (list[float]): First embedding vector.
        embedding_b (list[float]): Second embedding vector.
    Returns:
        float: Cosine similarity score in range [-1, 1].
    """
    a = np.array(embedding_a)
    b = np.array(embedding_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
