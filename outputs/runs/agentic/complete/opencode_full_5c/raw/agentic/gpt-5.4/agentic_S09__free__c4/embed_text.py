from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient


def embed_text(text: str, model: str = "embed-v4.0") -> list[float]:
    client = CohereEmbeddingsClient(model=model)
    response = client.embed([text], input_type="search_document")
    return response.embeddings[0].values
