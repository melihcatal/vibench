from __future__ import annotations

from translation_client import OPENAI_EMBEDDING_MODEL, openai_client
from translation_models import EmbeddingResult


def translation_memory_embedding(translated_segment: str) -> EmbeddingResult:
    response = openai_client().embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=translated_segment,
    )
    item = response.data[0]
    return EmbeddingResult(vector=list(item.embedding), model=response.model, raw=response.model_dump())
