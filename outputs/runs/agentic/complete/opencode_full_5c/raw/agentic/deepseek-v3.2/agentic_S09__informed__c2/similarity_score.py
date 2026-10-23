import numpy as np
from typing import List
from embed_text import embed_text


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        float: Cosine similarity score between -1 and 1
    """
    v1 = np.array(vec1)
    v2 = np.array(vec2)

    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def similarity_score(
    text1: str, text2: str, model: str = "text-embedding-3-small"
) -> float:
    """
    Compute cosine similarity between two embedded texts.

    Args:
        text1: First text string
        text2: Second text string
        model: The OpenAI embedding model identifier

    Returns:
        float: Cosine similarity score between -1 and 1
    """
    embedding1 = embed_text(text1, model)
    embedding2 = embed_text(text2, model)

    return cosine_similarity(embedding1, embedding2)
