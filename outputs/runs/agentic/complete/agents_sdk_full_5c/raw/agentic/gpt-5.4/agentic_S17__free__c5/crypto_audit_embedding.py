from __future__ import annotations

from security_client import DEFAULT_OPENAI_EMBED_MODEL, get_openai_client
from security_models import EmbeddingResult


def crypto_audit_embedding(note: str) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=DEFAULT_OPENAI_EMBED_MODEL,
        input=note,
    )
    embedding = response.data[0].embedding
    return EmbeddingResult(
        provider="openai",
        model=DEFAULT_OPENAI_EMBED_MODEL,
        vector=embedding,
    )
