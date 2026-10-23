from __future__ import annotations

from openai import OpenAI

from security_client import get_openai_api_key
from security_models import EmbeddingVector


def secret_audit_embedding(audit_notes: str) -> EmbeddingVector:
    client = OpenAI(api_key=get_openai_api_key())
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=audit_notes,
    )
    item = response.data[0]
    return EmbeddingVector(
        provider="openai",
        model="text-embedding-3-small",
        dimensions=len(item.embedding),
        vector=item.embedding,
        input_text=audit_notes,
    )
