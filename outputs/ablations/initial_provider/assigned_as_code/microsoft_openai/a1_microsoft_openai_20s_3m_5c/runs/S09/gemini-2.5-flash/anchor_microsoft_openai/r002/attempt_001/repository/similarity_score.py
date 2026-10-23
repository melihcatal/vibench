import numpy as np
from typing import List

def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    # Ensure the embeddings are numpy arrays
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    # Compute dot product
    dot_product = np.dot(vec1, vec2)

    # Compute magnitudes
    magnitude1 = np.linalg.norm(vec1)
    magnitude2 = np.linalg.norm(vec2)

    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)

def similarity_score(embedding1: List[float], embedding2: List[float]) -> float:
    return cosine_similarity(embedding1, embedding2)
