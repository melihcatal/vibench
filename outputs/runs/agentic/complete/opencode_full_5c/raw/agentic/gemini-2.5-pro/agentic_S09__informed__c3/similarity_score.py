import numpy as np
from embed_text import generate_embedding


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Computes cosine similarity between two embedded texts using OpenAI embeddings.
    """
    embedding1 = generate_embedding(text1)
    embedding2 = generate_embedding(text2)

    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    cosine_similarity = np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )
    return float(cosine_similarity)
