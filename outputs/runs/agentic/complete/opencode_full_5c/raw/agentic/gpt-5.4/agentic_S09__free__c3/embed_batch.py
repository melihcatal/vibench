from __future__ import annotations

from embeddings_client import OPENAI_EMBEDDINGS_MODEL, create_embeddings
from embeddings_models import normalize_texts


def embed_batch(
    texts: list[str],
    model: str = OPENAI_EMBEDDINGS_MODEL,
    dimensions: int | None = None,
) -> dict:
    normalized = normalize_texts(texts)
    result = create_embeddings(normalized, model=model, dimensions=dimensions)
    return {
        "provider": "OpenAI",
        "model": result.model,
        "embeddings": [item.embedding for item in result.vectors],
        "count": len(result.vectors),
        "usage": result.usage,
    }
