from __future__ import annotations

from security_client import get_openai_client
from security_models import EmbeddingResult, normalize_text


def crypto_audit_embedding(note: str) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=normalize_text(note),
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        provider="openai",
        model="text-embedding-3-large",
        vector=vector,
        dimensions=len(vector),
    )
