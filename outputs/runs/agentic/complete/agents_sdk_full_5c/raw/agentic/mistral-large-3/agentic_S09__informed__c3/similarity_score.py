from typing import List
import numpy as np
from embed_text import embed_text


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    arr1 = np.array(vec1, dtype=np.float32)
    arr2 = np.array(vec2, dtype=np.float32)
    dot_product = np.dot(arr1, arr2)
    norm1 = np.linalg.norm(arr1)
    norm2 = np.linalg.norm(arr2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(dot_product / (norm1 * norm2))


def similarity_score(text1: str, text2: str) -> float:
    """Compute cosine similarity between two embedded texts using Cohere."""
    vec1 = embed_text(text1)
    vec2 = embed_text(text2)
    return cosine_similarity(vec1, vec2)