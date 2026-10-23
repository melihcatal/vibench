import numpy as np
from typing import List


def similarity_score(embedding1: List[float], embedding2: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    # Normalize vectors to unit length
    vec1 = vec1 / np.linalg.norm(vec1)
    vec2 = vec2 / np.linalg.norm(vec2)

    return float(np.dot(vec1, vec2))
