from __future__ import annotations

from typing import Sequence

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings


def embed_batch(texts: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL, dimensions: int | None = None) -> list[list[float]]:
    response = create_embeddings(list(texts), model=model, dimensions=dimensions, input_type="search_document")
    return response.vectors()
