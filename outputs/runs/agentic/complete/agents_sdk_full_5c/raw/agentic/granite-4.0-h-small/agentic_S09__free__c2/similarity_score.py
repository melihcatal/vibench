# similarity_score.py
import numpy as np

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec_a (list[float]): embedding vector A.
        vec_b (list[float]): embedding vector B.

    Returns:
        float: cosine similarity in range [-1, 1].
    """
    a = np.array(vec_a)
    b = np.array(vec_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
