from __future__ import annotations

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embedding


def embed_text(text: str, model: str = DEFAULT_EMBEDDING_MODEL, dimensions: int | None = None) -> list[float]:
    response = create_embedding(text=text, model=model, dimensions=dimensions)
    return response.data[0].embedding
