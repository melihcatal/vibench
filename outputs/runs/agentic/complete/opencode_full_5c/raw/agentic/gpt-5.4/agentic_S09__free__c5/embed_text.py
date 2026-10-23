from __future__ import annotations

from embeddings_client import DEFAULT_EMBEDDING_MODEL, create_embedding


def embed_text(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> dict:
    result = create_embedding(text=text, model=model)
    return {
        "provider": "openai",
        "model": result.model,
        "embedding": result.first_vector(),
        "usage": result.usage,
    }
