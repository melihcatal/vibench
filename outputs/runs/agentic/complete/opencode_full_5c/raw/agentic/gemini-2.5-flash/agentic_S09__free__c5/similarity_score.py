from typing import List

from embeddings_models import cosine_similarity
from embed_text import embed_text


def similarity_score(text1: str, text2: str) -> float:
    """Computes the cosine similarity between two embedded texts.

    Args:
        text1: The first text string.
        text2: The second text string.

    Returns:
        The cosine similarity score.
    """
    embedding1 = embed_text(text1)
    embedding2 = embed_text(text2)
    return cosine_similarity(embedding1, embedding2)
