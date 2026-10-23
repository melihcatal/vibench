from __future__ import annotations

from translation_client import OPENAI_EMBEDDING_MODEL, openai_embedding
from translation_models import EmbeddingResult, ensure_text


def translation_memory_embedding(translated_segment: str) -> dict[str, object]:
    clean_segment = ensure_text(translated_segment)
    item = openai_embedding(clean_segment)
    result = EmbeddingResult(
        vector=item["embedding"],
        provider="openai",
        model=OPENAI_EMBEDDING_MODEL,
    )
    return {
        "vector": result.vector,
        "provider": result.provider,
        "model": result.model,
    }
