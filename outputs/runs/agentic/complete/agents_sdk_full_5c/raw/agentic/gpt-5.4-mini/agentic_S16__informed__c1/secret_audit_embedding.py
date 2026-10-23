from __future__ import annotations

import os

from openai import OpenAI


EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def secret_audit_embedding(notes: str) -> list[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    result = client.embeddings.create(model=EMBEDDING_MODEL, input=notes)
    return list(result.data[0].embedding)
