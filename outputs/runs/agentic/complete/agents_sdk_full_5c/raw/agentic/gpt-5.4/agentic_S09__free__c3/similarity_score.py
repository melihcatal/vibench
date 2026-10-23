from __future__ import annotations

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings
from embeddings_models import cosine_similarity


def similarity_score(text_a: str, text_b: str, model: str = DEFAULT_EMBEDDING_MODEL) -> dict:
    result = create_embeddings([text_a, text_b], model=model)
    score = cosine_similarity(result.vectors[0], result.vectors[1])
    return {
        "provider": "openai",
        "model": result.model,
        "similarity": score,
        "usage": result.usage,
    }
