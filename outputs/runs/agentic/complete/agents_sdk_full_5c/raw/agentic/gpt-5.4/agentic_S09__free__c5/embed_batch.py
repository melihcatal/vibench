from __future__ import annotations

from collections.abc import Iterable

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings


def embed_batch(texts: Iterable[str], model: str = DEFAULT_EMBEDDING_MODEL, dimensions: int | None = None) -> list[list[float]]:
    response = create_embeddings(texts=texts, model=model, dimensions=dimensions)
    return [item.embedding for item in sorted(response.data, key=lambda item: item.index)]
