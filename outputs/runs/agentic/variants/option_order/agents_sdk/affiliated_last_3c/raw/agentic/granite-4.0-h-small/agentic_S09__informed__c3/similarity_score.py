import numpy as np

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec_a (list[float]): First embedding vector.
        vec_b (list[float]): Second embedding vector.

    Returns:
        float: Cosine similarity in range [-1, 1].
    """
    a = np.array(vec_a)
    b = np.array(vec_b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
