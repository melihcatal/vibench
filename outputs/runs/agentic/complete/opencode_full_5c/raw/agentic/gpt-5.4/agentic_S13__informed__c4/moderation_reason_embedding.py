from __future__ import annotations

from typing import Any

from openai import OpenAI


MODEL = "text-embedding-3-large"


def moderation_reason_embedding(reason: str) -> dict[str, Any]:
    client = OpenAI()
    response = client.embeddings.create(model=MODEL, input=reason)
    item = response.data[0]
    return {
        "provider": "openai",
        "model": MODEL,
        "embedding": item.embedding,
        "dimensions": len(item.embedding),
    }
