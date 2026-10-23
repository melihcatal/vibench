import numpy as np
from typing import List

def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Computes the cosine similarity between two embedding vectors.

    Args:
        embedding1: The first embedding vector.
        embedding2: The second embedding vector.

    Returns:
        The cosine similarity score (a float between -1 and 1).
    """
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0

    return dot_product / (norm_vec1 * norm_vec2)

