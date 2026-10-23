import numpy as np

def compute_cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Computes the cosine similarity between two embedding vectors.

    Args:
        embedding1: A numpy array representing the first embedding.
        embedding2: A numpy array representing the second embedding.

    Returns:
        The cosine similarity as a float.
    """
    dot_product = np.dot(embedding1, embedding2)
    norm_embedding1 = np.linalg.norm(embedding1)
    norm_embedding2 = np.linalg.norm(embedding2)

    if norm_embedding1 == 0 or norm_embedding2 == 0:
        return 0.0  # Or handle as an error, depending on desired behavior

    return dot_product / (norm_embedding1 * norm_embedding2)
