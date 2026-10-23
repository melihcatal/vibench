from typing import List
import math
from embed_text import embed_text


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Computes the cosine similarity between two embedding vectors."""
    dot_product = sum(e1 * e2 for e1, e2 in zip(embedding1, embedding2))
    magnitude1 = math.sqrt(sum(e1 * e1 for e1 in embedding1))
    magnitude2 = math.sqrt(sum(e2 * e2 for e2 in embedding2))

    if not magnitude1 or not magnitude2:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)


def similarity_score(text1: str, text2: str) -> float:
    """Embeds two texts and computes the cosine similarity between their embeddings."""
    embedding1 = embed_text(text1)
    embedding2 = embed_text(text2)
    return cosine_similarity(embedding1, embedding2)
