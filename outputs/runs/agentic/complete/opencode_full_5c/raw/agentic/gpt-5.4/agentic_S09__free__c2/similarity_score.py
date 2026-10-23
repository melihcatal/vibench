from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient, DEFAULT_EMBED_MODEL
from embeddings_models import l2_normalize


def cosine_similarity_for_texts(
    text_a: str, text_b: str, model: str = DEFAULT_EMBED_MODEL
) -> float:
    client = CohereEmbeddingsClient()
    response = client.embed([text_a, text_b], model=model, input_type="search_document")
    if len(response.vectors) < 2:
        return 0.0
    a = l2_normalize(response.vectors[0].embedding)
    b = l2_normalize(response.vectors[1].embedding)
    return float(sum(left * right for left, right in zip(a, b)))
