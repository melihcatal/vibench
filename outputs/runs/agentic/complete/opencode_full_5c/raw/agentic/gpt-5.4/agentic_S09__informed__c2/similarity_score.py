from __future__ import annotations

from embed_text import embed_text
from embeddings_models import DEFAULT_EMBEDDING_MODEL, cosine_similarity


def similarity_score(
    text_a: str, text_b: str, model: str = DEFAULT_EMBEDDING_MODEL
) -> float:
    embedding_a = embed_text(text_a, model=model)
    embedding_b = embed_text(text_b, model=model)
    return cosine_similarity(embedding_a, embedding_b)
