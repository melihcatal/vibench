from typing import List
import numpy as np
from .embed_text import embed_text


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Computes cosine similarity between two vectors.

    Args:
        vec1: First embedding vector.
        vec2: Second embedding vector.

    Returns:
        Cosine similarity score between the two vectors.
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))


def similarity_score(
    text1: str, text2: str, model: str = "text-embedding-3-small"
) -> float:
    """
    Computes cosine similarity between two embedded texts using OpenAI's embeddings API.

    Args:
        text1: First input text.
        text2: Second input text.
        model: OpenAI embedding model to use (default: text-embedding-3-small).

    Returns:
        Cosine similarity score between the two texts.
    """
    embedding1 = embed_text(text1, model)
    embedding2 = embed_text(text2, model)
    return cosine_similarity(embedding1, embedding2)
