from __future__ import annotations

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embedding


def embed_text(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> dict:
    result = create_embedding(text=text, model=model)
    return {
        "provider": "openai",
        "model": result.model,
        "dimensions": len(result.vectors[0]) if result.vectors else 0,
        "embedding": result.vectors[0] if result.vectors else [],
        "usage": result.usage,
    }
