from __future__ import annotations

from embeddings_client import create_embeddings
from embeddings_models import cosine_similarity



def similarity_score(
    left_text: str,
    right_text: str,
    model: str = "text-embedding-3-small",
    dimensions: int | None = None,
) -> float:
    response = create_embeddings([left_text, right_text], model=model, dimensions=dimensions)
    left_vector = response.vectors[0].embedding
    right_vector = response.vectors[1].embedding
    return cosine_similarity(left_vector, right_vector)
