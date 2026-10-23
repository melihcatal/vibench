from __future__ import annotations

from embeddings_client import embed_texts
from embeddings_models import cosine_similarity


def score_similarity(text_a: str, text_b: str) -> float:
    response = embed_texts([text_a, text_b])
    return cosine_similarity(response.embeddings[0], response.embeddings[1])
