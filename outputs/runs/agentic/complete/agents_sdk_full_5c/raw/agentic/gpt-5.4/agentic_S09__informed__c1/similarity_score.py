from __future__ import annotations

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings
from embeddings_models import SimilarityResult, cosine_similarity


def similarity_score(
    left_text: str,
    right_text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: int | None = None,
) -> SimilarityResult:
    response = create_embeddings([left_text, right_text], model=model, dimensions=dimensions, input_type="search_document")
    left_vector = response.records[0].embedding
    right_vector = response.records[1].embedding
    score = cosine_similarity(left_vector, right_vector)
    return SimilarityResult(score=score, left_model=response.model, right_model=response.model, provider="openai")
