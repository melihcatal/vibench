from __future__ import annotations

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings


def embed_text(text: str, model: str = DEFAULT_EMBEDDING_MODEL, dimensions: int | None = None) -> list[float]:
    response = create_embeddings([text], model=model, dimensions=dimensions, input_type="search_document")
    return response.records[0].embedding
