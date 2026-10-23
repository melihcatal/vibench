from __future__ import annotations

import os

from openai import OpenAI


def crypto_audit_embedding(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.embeddings.create(model="text-embedding-3-small", input=text)
    return {"provider": "openai", "model": "text-embedding-3-small", "embedding": result.data[0].embedding}
