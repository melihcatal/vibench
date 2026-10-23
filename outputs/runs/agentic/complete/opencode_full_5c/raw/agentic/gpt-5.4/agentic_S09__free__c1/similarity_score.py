from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient
from embeddings_models import cosine_similarity, normalize_text


def similarity_score(left_text: str, right_text: str) -> dict[str, object]:
    client = CohereEmbeddingsClient()
    left = normalize_text(left_text)
    right = normalize_text(right_text)
    response = client.embed([left, right], input_type="search_document")
    score = cosine_similarity(response.embeddings[0], response.embeddings[1])
    return {
        "provider": "cohere",
        "model": client.model,
        "left_text": left,
        "right_text": right,
        "similarity": score,
    }
