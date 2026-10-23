from __future__ import annotations

from embeddings_client import create_embedding_request, fetch_embeddings


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_text(text: str, *, model: str = OPENAI_EMBEDDING_MODEL, dimensions: int | None = None) -> list[float]:
    request = create_embedding_request([text], model=model, dimensions=dimensions)
    response = fetch_embeddings(request)
    return response.vectors[0].embedding
