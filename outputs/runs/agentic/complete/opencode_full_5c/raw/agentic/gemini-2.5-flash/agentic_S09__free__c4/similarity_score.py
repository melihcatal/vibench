from typing import List
from embeddings_models import calculate_cosine_similarity


def compute_similarity_score(embedding1: List[float], embedding2: List[float]) -> float:
    """Computes cosine similarity between two embedded texts."""
    return calculate_cosine_similarity(embedding1, embedding2)
