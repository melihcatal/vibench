from __future__ import annotations

import os

from openai import OpenAI


def embed_secret_audit_notes(notes: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=notes,
    )
    item = response.data[0]
    return {
        "provider": "openai",
        "model": "text-embedding-3-large",
        "embedding": item.embedding,
        "dimensions": len(item.embedding),
    }
