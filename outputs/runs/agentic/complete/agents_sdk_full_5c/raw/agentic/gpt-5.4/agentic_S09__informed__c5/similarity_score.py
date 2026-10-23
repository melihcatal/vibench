from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient
from embeddings_models import cosine_similarity


def embedded_cosine_similarity(text_a: str, text_b: str) -> float:
    client = CohereEmbeddingsClient()
    result = client.embed_texts([text_a, text_b], input_type="search_document")
    return cosine_similarity(result.embeddings[0], result.embeddings[1])
