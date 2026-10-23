from __future__ import annotations

from embeddings_client import create_embeddings
from embeddings_models import cosine_similarity


def similarity_score(text_a: str, text_b: str, model: str = "embed-v4.0") -> float:
    response = create_embeddings(
        [text_a, text_b], model=model, input_type="search_document"
    )
    first = response.results[0].embedding
    second = response.results[1].embedding
    return cosine_similarity(first, second)
