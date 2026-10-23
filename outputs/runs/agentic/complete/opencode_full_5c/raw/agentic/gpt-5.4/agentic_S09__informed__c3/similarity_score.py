from __future__ import annotations

import math

from embeddings_client import DEFAULT_EMBED_MODEL, create_embeddings
from embeddings_models import normalize_text


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        raise ValueError("embedding vectors must not be zero")
    return numerator / (left_norm * right_norm)


def similarity_score(
    text_a: str, text_b: str, model: str = DEFAULT_EMBED_MODEL
) -> float:
    response = create_embeddings(
        [normalize_text(text_a), normalize_text(text_b)],
        model=model,
        input_type="search_document",
    )
    return _cosine_similarity(response.embeddings[0], response.embeddings[1])
