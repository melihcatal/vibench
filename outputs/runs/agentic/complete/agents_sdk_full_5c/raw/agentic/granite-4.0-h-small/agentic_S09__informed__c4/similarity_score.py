# similarity_score.py

import math

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec1 (List[float]): First embedding vector.
        vec2 (List[float]): Second embedding vector.

    Returns:
        float: Cosine similarity score in range [-1, 1].
    """
    if len(vec1) != len(vec2):
        raise ValueError("Embedding vectors must be the same length")
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)
