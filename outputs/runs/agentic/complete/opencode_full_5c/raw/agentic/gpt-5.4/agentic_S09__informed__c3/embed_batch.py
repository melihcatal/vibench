from __future__ import annotations

from embeddings_client import DEFAULT_EMBED_MODEL, create_embeddings
from embeddings_models import normalize_texts


def embed_batch(
    texts: list[str], model: str = DEFAULT_EMBED_MODEL
) -> list[list[float]]:
    response = create_embeddings(
        normalize_texts(texts), model=model, input_type="search_document"
    )
    return response.embeddings
