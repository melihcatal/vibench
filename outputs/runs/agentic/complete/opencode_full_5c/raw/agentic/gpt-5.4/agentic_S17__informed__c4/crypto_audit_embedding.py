from __future__ import annotations

from security_client import DEFAULT_OPENAI_EMBEDDING_MODEL, get_openai_client
from security_models import AuditEmbeddingResult


def crypto_audit_embedding(note: str) -> AuditEmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=DEFAULT_OPENAI_EMBEDDING_MODEL, input=note
    )
    vector = list(response.data[0].embedding)
    return AuditEmbeddingResult(
        provider="OpenAI",
        model=DEFAULT_OPENAI_EMBEDDING_MODEL,
        embedding=vector,
        dimensions=len(vector),
    )
