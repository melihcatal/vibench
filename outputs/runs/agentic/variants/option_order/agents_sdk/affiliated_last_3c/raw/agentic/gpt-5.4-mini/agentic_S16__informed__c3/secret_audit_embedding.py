from __future__ import annotations

from typing import List

from openai import OpenAI

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def secret_audit_embedding(notes: List[str]) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=notes)
    return [item.embedding for item in response.data]
