import math
from embeddings_models import normalize_vector


def similarity_score(vec1: list[float], vec2: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec1 (list[float]): First embedding vector.
        vec2 (list[float]): Second embedding vector.

    Returns:
        float: Cosine similarity score between -1 and 1.
    """
    if len(vec1) != len(vec2):
        raise ValueError('Embedding vectors must be the same dimension')
    # Normalize vectors (optional, since normalize_vector ensures unit length)
    u = normalize_vector(vec1)
    v = normalize_vector(vec2)
    # Dot product
    return sum(a * b for a, b in zip(u, v))
