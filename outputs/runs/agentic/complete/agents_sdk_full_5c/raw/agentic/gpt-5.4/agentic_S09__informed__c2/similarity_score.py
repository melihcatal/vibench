from __future__ import annotations

from embeddings_client import OPENAI_EMBEDDING_MODEL, create_embeddings
from embeddings_models import cosine_similarity


def similarity_score(text_a: str, text_b: str, *, model: str = OPENAI_EMBEDDING_MODEL, dimensions: int | None = None) -> float:
    response = create_embeddings([text_a, text_b], model=model, dimensions=dimensions)
    vectors = [vector.embedding for vector in sorted(response.vectors, key=lambda item: item.index)]
    return cosine_similarity(vectors[0], vectors[1])
