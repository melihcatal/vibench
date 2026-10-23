from __future__ import annotations

from collections.abc import Sequence

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings


def embed_batch(texts: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> dict:
    result = create_embeddings(texts=texts, model=model)
    return {
        "provider": "openai",
        "model": result.model,
        "count": len(result.vectors),
        "dimensions": len(result.vectors[0]) if result.vectors else 0,
        "embeddings": result.vectors,
        "usage": result.usage,
    }
