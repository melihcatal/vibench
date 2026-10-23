from __future__ import annotations

from embeddings_client import OPENAI_EMBEDDINGS_MODEL, create_embeddings
from embeddings_models import cosine_similarity, normalize_text


def similarity_score(
    text_a: str, text_b: str, model: str = OPENAI_EMBEDDINGS_MODEL
) -> dict:
    normalized_a = normalize_text(text_a)
    normalized_b = normalize_text(text_b)
    result = create_embeddings([normalized_a, normalized_b], model=model)
    if len(result.vectors) < 2:
        score = 0.0
        embeddings: list[list[float]] = []
    else:
        embeddings = [result.vectors[0].embedding, result.vectors[1].embedding]
        score = cosine_similarity(embeddings[0], embeddings[1])
    return {
        "provider": "OpenAI",
        "model": result.model,
        "text_a": normalized_a,
        "text_b": normalized_b,
        "similarity": score,
        "usage": result.usage,
    }
