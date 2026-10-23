import math
from embeddings_models import normalize_embedding
from typing import List


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Computes the cosine similarity between two embedding vectors."""
    embedding1_norm = normalize_embedding(embedding1)
    embedding2_norm = normalize_embedding(embedding2)

    dot_product = sum(v1 * v2 for v1, v2 in zip(embedding1_norm, embedding2_norm))
    return dot_product
