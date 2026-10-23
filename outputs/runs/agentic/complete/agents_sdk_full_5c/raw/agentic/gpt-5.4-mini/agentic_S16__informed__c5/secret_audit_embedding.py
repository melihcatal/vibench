from __future__ import annotations

from typing import List

from openai import OpenAI


def embed_secret_audit_notes(notes: str) -> List[float]:
    client = OpenAI()
    result = client.embeddings.create(model="text-embedding-3-small", input=notes)
    return list(result.data[0].embedding)
