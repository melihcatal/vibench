from __future__ import annotations

from embeddings_client import embed_texts
from embeddings_models import cosine_similarity, ensure_text


def score_text_similarity(
    left_text: str, right_text: str, model: str | None = None
) -> dict:
    texts = [ensure_text(left_text), ensure_text(right_text)]
    response = embed_texts(texts, input_type="search_document", model=model)
    score = cosine_similarity(response.embeddings[0], response.embeddings[1])
    return {
        "provider": "cohere",
        "model": response.model,
        "left_text": left_text,
        "right_text": right_text,
        "similarity": score,
    }
