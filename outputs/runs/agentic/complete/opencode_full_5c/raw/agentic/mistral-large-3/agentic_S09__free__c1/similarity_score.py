import numpy as np
from typing import List


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Computes the cosine similarity between two embedding vectors.

    Args:
        vec1: First embedding vector.
        vec2: Second embedding vector.

    Returns:
        Cosine similarity score between -1 and 1.
    """
    vec1_array = np.array(vec1)
    vec2_array = np.array(vec2)

    dot_product = np.dot(vec1_array, vec2_array)
    norm_vec1 = np.linalg.norm(vec1_array)
    norm_vec2 = np.linalg.norm(vec2_array)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0

    return float(dot_product / (norm_vec1 * norm_vec2))


def similarity_score(
    text1_embedding: List[float], text2_embedding: List[float]
) -> float:
    """
    Computes the cosine similarity score between two embedded texts.

    Args:
        text1_embedding: Embedding vector of the first text.
        text2_embedding: Embedding vector of the second text.

    Returns:
        Cosine similarity score between the two embeddings.
    """
    return cosine_similarity(text1_embedding, text2_embedding)
