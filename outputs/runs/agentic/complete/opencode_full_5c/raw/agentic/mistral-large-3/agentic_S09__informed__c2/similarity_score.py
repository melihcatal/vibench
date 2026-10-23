import numpy as np
from typing import List

from embeddings_models import normalize_embedding


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.
    Vectors are normalized before computation.
    """
    emb1 = normalize_embedding(embedding1)
    emb2 = normalize_embedding(embedding2)
    return np.dot(emb1, emb2).item()


def similarity_score(
    text_embedding1: List[float], text_embedding2: List[float]
) -> float:
    """
    Compute cosine similarity between two embedded texts.
    """
    return cosine_similarity(text_embedding1, text_embedding2)
