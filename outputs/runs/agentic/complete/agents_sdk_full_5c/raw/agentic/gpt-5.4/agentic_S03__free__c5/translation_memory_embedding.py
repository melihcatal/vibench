from __future__ import annotations

from translation_client import OPENAI_EMBEDDING_MODEL, get_openai_client
from translation_models import EmbeddingResult


def embed_translated_segment(text: str) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=text,
    )
    item = response.data[0]
    vector = list(item.embedding)
    return EmbeddingResult(
        vector=vector,
        dimensions=len(vector),
        provider="openai",
        model=OPENAI_EMBEDDING_MODEL,
        raw=response.model_dump(),
    )
