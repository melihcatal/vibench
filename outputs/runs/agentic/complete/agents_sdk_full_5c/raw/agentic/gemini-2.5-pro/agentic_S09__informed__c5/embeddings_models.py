import numpy as np
from typing import List

# A simple data class could be defined here if needed,
# but for this scope, direct dictionary and list manipulation is sufficient.

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """
    Computes the cosine similarity between two vectors.
    """
    vec1 = np.array(v1)
    vec2 = np.array(v2)
    
    # Check for zero vectors
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0

    # Using numpy for efficient computation
    similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return float(similarity)

