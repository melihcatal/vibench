from __future__ import annotations

from embed_text import embed_text
from embeddings_models import cosine_similarity


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def similarity_score(
    text_a: str,
    text_b: str,
    *,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: int | None = None,
) -> float:
    vector_a = embed_text(text_a, model=model, dimensions=dimensions)
    vector_b = embed_text(text_b, model=model, dimensions=dimensions)
    return cosine_similarity(vector_a, vector_b)
