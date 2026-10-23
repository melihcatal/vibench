from __future__ import annotations

from translation_client import get_openai_client
from translation_models import EmbeddingResult


def embed_translated_segment(text: str) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        embedding=vector,
        dimensions=len(vector),
        provider="openai",
        model="text-embedding-3-small",
        raw=response.model_dump(),
    )
