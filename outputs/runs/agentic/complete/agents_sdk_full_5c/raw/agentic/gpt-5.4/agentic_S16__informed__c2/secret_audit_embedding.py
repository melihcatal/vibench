from __future__ import annotations

import os

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"


def embed_audit_note(note: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=note,
    )
    item = response.data[0]
    return {
        "provider": "openai",
        "model": EMBEDDING_MODEL,
        "dimensions": len(item.embedding),
        "embedding": item.embedding,
    }
