from __future__ import annotations

import openai

from security_models import EmbeddingRecord


EMBEDDING_MODEL = "text-embedding-3-small"


def embed_audit_note(note: str) -> EmbeddingRecord:
    client = openai.OpenAI()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=note,
    )
    item = response.data[0]
    return EmbeddingRecord(text=note, vector=item.embedding, model=EMBEDDING_MODEL)
