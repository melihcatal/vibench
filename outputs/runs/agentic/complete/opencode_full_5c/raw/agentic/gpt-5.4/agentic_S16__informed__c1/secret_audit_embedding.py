from __future__ import annotations

from security_client import get_openai_client
from security_models import EmbeddingResult


def embed_secret_audit_notes(text: str) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    item = response.data[0]
    return EmbeddingResult(text=text, vector=list(item.embedding), model=response.model)
