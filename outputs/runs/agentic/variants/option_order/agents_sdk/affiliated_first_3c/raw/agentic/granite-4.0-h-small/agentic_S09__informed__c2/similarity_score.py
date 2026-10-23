import os
import math
from embeddings_client import get_embedder
from embeddings_models import normalize_similarity

def similarity_score(vec1: list[float], vec2: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors using the configured provider."""
    norm1 = normalize_similarity(vec1)
    norm2 = normalize_similarity(vec2)
    return sum(a * b for a, b in zip(norm1, norm2))
