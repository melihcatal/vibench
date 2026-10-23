from __future__ import annotations

from collections.abc import Sequence

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embeddings


def embed_batch(texts: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> dict:
    result = create_embeddings(texts=texts, model=model)
    return {
        "provider": "openai",
        "model": result.model,
        "embeddings": [record.embedding for record in result.records],
        "usage": result.usage,
    }
