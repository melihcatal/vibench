from __future__ import annotations

from security_client import openai_client
from security_models import EmbeddingResult


MODEL = "text-embedding-3-large"


def embed_crypto_audit_notes(notes: str) -> EmbeddingResult:
    client = openai_client()
    response = client.embeddings.create(
        model=MODEL,
        input=notes,
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        provider="openai",
        model=MODEL,
        vector=vector,
        dimensions=len(vector),
    )
