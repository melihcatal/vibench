from __future__ import annotations

from security_client import openai_client
from security_models import EmbeddingResult


def crypto_audit_embedding(note: str) -> EmbeddingResult:
    client = openai_client()
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=note,
    )
    item = response.data[0]
    return EmbeddingResult(model=response.model, vector=list(item.embedding))
