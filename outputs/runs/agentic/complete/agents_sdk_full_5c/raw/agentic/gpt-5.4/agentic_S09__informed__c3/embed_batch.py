from __future__ import annotations

from embeddings_client import create_embeddings



def embed_batch(texts: list[str], model: str = "text-embedding-3-small", dimensions: int | None = None) -> list[list[float]]:
    response = create_embeddings(texts, model=model, dimensions=dimensions)
    return response.embeddings
