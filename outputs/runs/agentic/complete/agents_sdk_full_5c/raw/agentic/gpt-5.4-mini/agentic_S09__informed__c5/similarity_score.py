from __future__ import annotations

from embeddings_models import cosine_similarity
from embed_text import embed_text


def similarity_score(text_a: str, text_b: str, model: str | None = None) -> float:
    a = embed_text(text_a, model=model).embedding
    b = embed_text(text_b, model=model).embedding
    return cosine_similarity(a, b)
