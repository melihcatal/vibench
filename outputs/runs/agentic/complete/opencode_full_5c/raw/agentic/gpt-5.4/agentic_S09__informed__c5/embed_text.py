from __future__ import annotations

from embeddings_client import embed_texts
from embeddings_models import ensure_text


def generate_embedding(text: str, model: str | None = None) -> dict:
    response = embed_texts(
        [ensure_text(text)], input_type="search_document", model=model
    )
    return {
        "provider": "cohere",
        "model": response.model,
        "text": text,
        "embedding": response.embeddings[0],
        "dimensions": len(response.embeddings[0]),
    }
