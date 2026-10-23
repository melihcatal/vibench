from __future__ import annotations

from embeddings_client import DEFAULT_EMBED_MODEL, create_embeddings
from embeddings_models import normalize_text


def embed_text(text: str, model: str = DEFAULT_EMBED_MODEL) -> list[float]:
    response = create_embeddings(
        [normalize_text(text)], model=model, input_type="search_document"
    )
    return response.embeddings[0]
