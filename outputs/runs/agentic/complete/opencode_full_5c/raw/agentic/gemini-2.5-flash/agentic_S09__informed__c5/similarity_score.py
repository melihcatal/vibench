import numpy as np
from embed_text import embed_text


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Computes the cosine similarity between two vectors."""
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)
    dot_product = np.dot(vec1_np, vec2_np)
    norm_a = np.linalg.norm(vec1_np)
    norm_b = np.linalg.norm(vec2_np)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def similarity_score(text1: str, text2: str) -> float:
    """Computes the cosine similarity between embeddings of two texts."""
    embedding1 = embed_text(text1)
    embedding2 = embed_text(text2)

    if not embedding1 or not embedding2:
        print("Could not generate embeddings for one or both texts.")
        return 0.0

    return cosine_similarity(embedding1, embedding2)
