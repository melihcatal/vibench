from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient


def embed_batch(texts: list[str], model: str = "embed-v4.0") -> list[list[float]]:
    client = CohereEmbeddingsClient(model=model)
    response = client.embed(texts, input_type="search_document")
    return [item.values for item in response.embeddings]
