from __future__ import annotations

from collections.abc import Sequence

from embeddings_client import create_embedding_request, fetch_embeddings


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_batch(
    texts: Sequence[str],
    *,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: int | None = None,
) -> list[list[float]]:
    request = create_embedding_request(texts, model=model, dimensions=dimensions)
    response = fetch_embeddings(request)
    return [item.embedding for item in sorted(response.vectors, key=lambda item: item.index)]
