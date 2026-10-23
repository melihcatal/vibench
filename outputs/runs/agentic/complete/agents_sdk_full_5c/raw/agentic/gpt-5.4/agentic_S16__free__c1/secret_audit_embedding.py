from __future__ import annotations

from security_client import get_openai_client
from security_models import EmbeddingResult


EMBEDDING_MODEL = "text-embedding-3-small"



def secret_audit_embedding(audit_notes: str) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=audit_notes)
    return EmbeddingResult(
        provider="OpenAI",
        model=EMBEDDING_MODEL,
        vector=response.data[0].embedding,
    )
