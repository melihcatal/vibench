from __future__ import annotations

from typing import List

from openai import OpenAI

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_crypto_audit_notes(notes: List[str]) -> list[list[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=notes)
    return [item.embedding for item in response.data]
