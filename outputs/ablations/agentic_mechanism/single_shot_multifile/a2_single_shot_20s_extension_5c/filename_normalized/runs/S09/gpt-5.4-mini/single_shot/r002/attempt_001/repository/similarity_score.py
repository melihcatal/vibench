from math import sqrt
from typing import List

from embeddings_models import cosine_similarity as _cosine_similarity, validate_embedding


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    validate_embedding(vec_a)
    validate_embedding(vec_b)
    return _cosine_similarity(vec_a, vec_b)
