from __future__ import annotations

from security_client import openai_client
from security_models import AuditEmbeddingResult


def crypto_audit_embedding(note: str) -> AuditEmbeddingResult:
    client = openai_client()
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=note,
    )
    vector = list(response.data[0].embedding)
    return AuditEmbeddingResult(
        provider="openai",
        model="text-embedding-3-large",
        dimensions=len(vector),
        embedding=vector,
    )
