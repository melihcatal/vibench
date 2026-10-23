import numpy as np

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Computes the cosine similarity between two vectors.

    Args:
        vec1: The first vector.
        vec2: The second vector.

    Returns:
        The cosine similarity score.
    """
    if not isinstance(vec1, np.ndarray) or not isinstance(vec2, np.ndarray):
        raise TypeError("Input vectors must be numpy arrays.")
    
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
        
    return dot_product / (norm_vec1 * norm_vec2)
