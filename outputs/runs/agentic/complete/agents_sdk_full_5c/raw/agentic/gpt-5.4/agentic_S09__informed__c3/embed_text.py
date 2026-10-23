from __future__ import annotations

from embeddings_client import create_embeddings



def embed_text(text: str, model: str = "text-embedding-3-small", dimensions: int | None = None) -> list[float]:
    response = create_embeddings([text], model=model, dimensions=dimensions)
    return response.vectors[0].embedding
