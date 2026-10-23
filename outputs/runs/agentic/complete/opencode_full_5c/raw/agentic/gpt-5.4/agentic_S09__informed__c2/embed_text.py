from __future__ import annotations

from embeddings_client import create_embeddings
from embeddings_models import DEFAULT_EMBEDDING_MODEL, normalize_text


def embed_text(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> list[float]:
    response = create_embeddings([normalize_text(text)], model=model)
    return response.items[0].embedding
