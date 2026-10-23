from __future__ import annotations

from embeddings_client import embed_texts
from embeddings_models import ensure_texts


def generate_batch_embeddings(texts: list[str], model: str | None = None) -> dict:
    normalized = ensure_texts(texts)
    response = embed_texts(normalized, input_type="search_document", model=model)
    return {
        "provider": "cohere",
        "model": response.model,
        "count": len(normalized),
        "items": [
            {
                "text": text,
                "embedding": embedding,
                "dimensions": len(embedding),
            }
            for text, embedding in zip(normalized, response.embeddings)
        ],
    }
