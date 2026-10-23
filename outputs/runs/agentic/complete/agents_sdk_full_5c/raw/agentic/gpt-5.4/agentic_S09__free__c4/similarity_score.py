from __future__ import annotations

from embeddings_client import DEFAULT_EMBEDDING_MODEL
from embeddings_models import cosine_similarity
from embed_text import embed_text


def similarity_score(text_a: str, text_b: str, model: str = DEFAULT_EMBEDDING_MODEL) -> float:
    vector_a = embed_text(text_a, model=model)
    vector_b = embed_text(text_b, model=model)
    return cosine_similarity(vector_a, vector_b)
