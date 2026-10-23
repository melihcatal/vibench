from __future__ import annotations

import os
from typing import List

from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"


def embed_secret_audit_notes(notes: List[str]) -> list[list[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    result = client.embeddings.create(model=EMBEDDING_MODEL, input=notes)
    return [item.embedding for item in result.data]
