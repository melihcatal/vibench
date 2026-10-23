from __future__ import annotations

from embeddings_client import OPENAI_EMBEDDING_MODEL, create_embedding


def embed_text(text: str, *, model: str = OPENAI_EMBEDDING_MODEL, dimensions: int | None = None) -> list[float]:
    response = create_embedding(text, model=model, dimensions=dimensions)
    return response.vectors[0].embedding
