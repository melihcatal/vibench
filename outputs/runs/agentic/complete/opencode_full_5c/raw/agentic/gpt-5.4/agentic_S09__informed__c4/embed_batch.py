from __future__ import annotations

from embeddings_client import create_embeddings


def embed_batch(texts: list[str], model: str = "embed-v4.0") -> list[list[float]]:
    response = create_embeddings(texts, model=model, input_type="search_document")
    return [item.embedding for item in response.results]
