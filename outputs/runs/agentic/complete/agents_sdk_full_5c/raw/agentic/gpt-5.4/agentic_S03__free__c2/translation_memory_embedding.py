from __future__ import annotations

from translation_client import OPENAI_EMBEDDING_MODEL, OPENAI_PROVIDER, get_openai_client
from translation_models import EmbeddingResult


def translation_memory_embedding(text: str) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=text,
    )
    return EmbeddingResult(
        vector=list(response.data[0].embedding),
        provider=OPENAI_PROVIDER,
        model=OPENAI_EMBEDDING_MODEL,
    )
