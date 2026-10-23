from typing import List
from embeddings_models import cosine_similarity


def similarity_score(embedding_a: List[float], embedding_b: List[float]) -> float:
    return cosine_similarity(embedding_a, embedding_b)
