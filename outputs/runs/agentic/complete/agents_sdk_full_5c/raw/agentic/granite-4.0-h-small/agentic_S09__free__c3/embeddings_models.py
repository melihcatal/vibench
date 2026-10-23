from typing import List

def normalize_embedding(vector: List[float]) -> List[float]:
    """L2-normalize an embedding vector.

    Args:
        vector: List of float values.
    Returns:
        L2-normalized vector with the same length.
    """
    norm = sum(v * v for v in vector) ** 0.5
    if norm == 0:
        return vector
    return [v / norm for v in vector]
