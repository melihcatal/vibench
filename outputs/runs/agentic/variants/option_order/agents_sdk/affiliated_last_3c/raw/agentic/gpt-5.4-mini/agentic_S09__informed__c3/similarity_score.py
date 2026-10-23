from __future__ import annotations

from embeddings_client import cosine_similarity, embed_text
from embeddings_models import normalize_text


def similarity_score(text_a: str, text_b: str) -> float:
    vector_a = embed_text(normalize_text(text_a))
    vector_b = embed_text(normalize_text(text_b))
    return cosine_similarity(vector_a, vector_b)
