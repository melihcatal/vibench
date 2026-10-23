import numpy as np

VERTEX_AI_EMBEDDING_MODEL = "text-embedding-004"

def compute_cosine_similarity(embedding1: list[float], embedding2: list[float]) -> float:
    """
    Computes the cosine similarity between two embedding vectors.

    Args:
        embedding1: The first embedding vector.
        embedding2: The second embedding vector.

    Returns:
        The cosine similarity between the two vectors.
    """
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return dot_product / (norm_vec1 * norm_vec2)
