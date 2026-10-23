from __future__ import annotations

from translation_client import DEFAULT_EMBEDDING_MODEL, get_openai_client
from translation_models import EmbeddingResult


def translation_memory_embedding(translated_segment: str) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=DEFAULT_EMBEDDING_MODEL,
        input=translated_segment,
    )
    vector = response.data[0].embedding
    return EmbeddingResult(vector=vector, dimensions=len(vector))
