from __future__ import annotations

import os

from openai import OpenAI


MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_secret_audit_notes(note_text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model=MODEL,
        input=note_text,
    )
    item = response.data[0]
    return {
        "provider": "OpenAI",
        "model": MODEL,
        "embedding": item.embedding,
        "dimensions": len(item.embedding),
    }
