from __future__ import annotations

from security_client import openai_client
from security_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def crypto_audit_embedding(note_text: str) -> EmbeddingResult:
    client = openai_client()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=note_text,
    )
    return EmbeddingResult(
        model=OPENAI_EMBEDDING_MODEL,
        vector=response.data[0].embedding,
        provider="openai",
    )
