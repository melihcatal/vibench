from __future__ import annotations

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings
from embeddings_models import cosine_similarity


def similarity_score(
    text_a: str, text_b: str, model: str = DEFAULT_EMBEDDING_MODEL
) -> dict:
    result = create_embeddings([text_a, text_b], model=model)
    if len(result.records) != 2:
        raise ValueError("Expected exactly two embeddings")
    vector_a = result.records[0].embedding
    vector_b = result.records[1].embedding
    return {
        "provider": "openai",
        "model": result.model,
        "similarity": cosine_similarity(vector_a, vector_b),
    }
