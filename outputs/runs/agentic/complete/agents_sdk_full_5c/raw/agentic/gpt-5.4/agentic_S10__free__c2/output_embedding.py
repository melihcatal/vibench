from __future__ import annotations

from model_client import DEFAULT_EMBEDDING_MODEL, create_embedding


def embed_output(text: str) -> dict:
    result = create_embedding(text, model=DEFAULT_EMBEDDING_MODEL)
    return {
        "provider": "openai",
        "model": DEFAULT_EMBEDDING_MODEL,
        "dimensions": len(result.vector),
        "embedding": result.vector,
    }
