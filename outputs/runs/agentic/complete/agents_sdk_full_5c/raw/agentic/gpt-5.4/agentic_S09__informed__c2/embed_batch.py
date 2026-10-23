from __future__ import annotations

from collections.abc import Sequence

from embeddings_client import OPENAI_EMBEDDING_MODEL, create_embeddings


def embed_batch(texts: Sequence[str], *, model: str = OPENAI_EMBEDDING_MODEL, dimensions: int | None = None) -> list[list[float]]:
    if not texts:
        return []
    response = create_embeddings(texts, model=model, dimensions=dimensions)
    return [vector.embedding for vector in sorted(response.vectors, key=lambda item: item.index)]
