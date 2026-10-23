from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient
from embeddings_models import normalize_embedding


def generate_text_embedding(text: str, *, normalize: bool = False) -> list[float]:
    client = CohereEmbeddingsClient()
    result = client.embed_texts(text, input_type="search_document")
    vector = result.embeddings[0]
    return normalize_embedding(vector) if normalize else vector
