from __future__ import annotations

from embeddings_models import cosine_similarity
from embed_text import embed_text


def similarity_score(text_a: str, text_b: str) -> float:
    embedding_a = embed_text(text_a).embedding
    embedding_b = embed_text(text_b).embedding
    return cosine_similarity(embedding_a, embedding_b)
