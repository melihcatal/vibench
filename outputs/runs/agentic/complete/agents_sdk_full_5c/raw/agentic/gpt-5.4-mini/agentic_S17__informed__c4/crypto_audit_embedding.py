from __future__ import annotations

from openai import OpenAI

from security_models import EmbeddingRecord, normalize_text


EMBEDDING_MODEL = "text-embedding-3-large"


def crypto_audit_embedding(note: str) -> EmbeddingRecord:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=normalize_text(note))
    embedding = response.data[0].embedding
    return EmbeddingRecord(text=normalize_text(note), embedding=embedding, provider="openai")
