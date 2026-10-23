from __future__ import annotations

from embeddings_client import create_embeddings


def embed_text(text: str, model: str = "embed-v4.0") -> list[float]:
    response = create_embeddings([text], model=model, input_type="search_document")
    return response.results[0].embedding
