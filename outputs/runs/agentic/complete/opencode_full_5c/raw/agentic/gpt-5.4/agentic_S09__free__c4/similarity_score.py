from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient
from embeddings_models import cosine_similarity


def similarity_score(
    left_text: str, right_text: str, model: str = "embed-v4.0"
) -> float:
    client = CohereEmbeddingsClient(model=model)
    response = client.embed([left_text, right_text], input_type="search_document")
    left_vector, right_vector = [item.values for item in response.embeddings[:2]]
    return cosine_similarity(left_vector, right_vector)
