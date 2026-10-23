from __future__ import annotations

from embeddings_client import OPENAI_EMBEDDINGS_MODEL, create_embeddings
from embeddings_models import normalize_text


def embed_text(
    text: str, model: str = OPENAI_EMBEDDINGS_MODEL, dimensions: int | None = None
) -> dict:
    normalized = normalize_text(text)
    result = create_embeddings(normalized, model=model, dimensions=dimensions)
    vector = result.vectors[0].embedding if result.vectors else []
    return {
        "provider": "OpenAI",
        "model": result.model,
        "input_text": normalized,
        "embedding": vector,
        "usage": result.usage,
    }
