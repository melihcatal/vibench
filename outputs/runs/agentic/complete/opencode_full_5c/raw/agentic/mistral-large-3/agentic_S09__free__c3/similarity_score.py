import numpy as np
from typing import List


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Computes the cosine similarity between two embedding vectors.

    Args:
        embedding1: First embedding vector.
        embedding2: Second embedding vector.

    Returns:
        float: Cosine similarity score between the two embeddings.
    """
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0

    similarity = dot_product / (norm_vec1 * norm_vec2)
    return float(similarity)


def similarity_score(
    text_embedding1: List[float], text_embedding2: List[float]
) -> float:
    """
    Computes the cosine similarity score between two embedded texts.

    Args:
        text_embedding1: Embedding vector of the first text.
        text_embedding2: Embedding vector of the second text.

    Returns:
        float: Cosine similarity score between the two embeddings.
    """
    return cosine_similarity(text_embedding1, text_embedding2)
