import numpy as np
from embed_text import embed_text


def similarity_score(
    text1: str, text2: str, model: str = "text-embedding-3-small"
) -> float:
    """
    Compute cosine similarity between two embedded texts.

    Args:
        text1: First text string
        text2: Second text string
        model: The embedding model to use (default: text-embedding-3-small)

    Returns:
        Cosine similarity score between -1 and 1
    """
    embedding1 = embed_text(text1, model)
    embedding2 = embed_text(text2, model)

    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    cosine_similarity = np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )
    return float(cosine_similarity)
