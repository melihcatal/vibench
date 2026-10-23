from __future__ import annotations

from collections.abc import Sequence

from embeddings_client import create_embeddings
from embeddings_models import DEFAULT_EMBEDDING_MODEL, normalize_texts


def embed_batch(
    texts: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL
) -> list[list[float]]:
    response = create_embeddings(normalize_texts(texts), model=model)
    return [
        item.embedding for item in sorted(response.items, key=lambda item: item.index)
    ]
