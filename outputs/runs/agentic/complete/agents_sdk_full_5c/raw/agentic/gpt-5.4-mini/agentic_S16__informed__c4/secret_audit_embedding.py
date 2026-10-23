from __future__ import annotations

from typing import List

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"


def embed_secret_audit_notes(notes: List[str]) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=notes)
    return [item.embedding for item in response.data]
