from __future__ import annotations

from openai import OpenAI

from security_models import EmbeddingResult, join_text_fields


EMBEDDING_MODEL = "text-embedding-3-small"


def embed_secret_audit_notes(secret_name: str, audit_notes: str, remediation_notes: str | None = None) -> EmbeddingResult:
    text = join_text_fields([f"Secret: {secret_name}", audit_notes, remediation_notes])
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    vector = list(response.data[0].embedding)
    return EmbeddingResult(model=EMBEDDING_MODEL, dimensions=len(vector), vector=vector)
