import numpy as np
from typing import List


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec1, vec2: Lists of floats representing embedding vectors.
    Returns:
        Similarity score in range [-1, 1].
    """
    arr1 = np.array(vec1, dtype=np.float32)
    arr2 = np.array(vec2, dtype=np.float32)
    dot_product = np.dot(arr1, arr2)
    norm1 = np.linalg.norm(arr1)
    norm2 = np.linalg.norm(arr2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def batch_similarity(
    query_embeddings: List[List[float]], document_embeddings: List[List[float]]
) -> List[float]:
    """Compute similarity scores between each query vector and each document vector.

    Args:
        query_embeddings: List of query vectors.
        document_embeddings: List of document vectors.
    Returns:
        List of similarity scores where each score corresponds to a query vector.
    """
    scores = []
    for q in query_embeddings:
        # Find the maximum similarity to any document vector (simplest matching strategy)
        max_sim = max(cosine_similarity(q, d) for d in document_embeddings)
        scores.append(max_sim)
    return scores
