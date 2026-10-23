import numpy as np
from typing import List
from embed_text import embed_text


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Computes the cosine similarity between two embedding vectors."""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def similarity_score(text1: str, text2: str) -> float:
    """Computes cosine similarity between two embedded texts using Google Gemini Embeddings."""
    embedding1 = embed_text(text1)
    embedding2 = embed_text(text2)
    return cosine_similarity(embedding1, embedding2)
