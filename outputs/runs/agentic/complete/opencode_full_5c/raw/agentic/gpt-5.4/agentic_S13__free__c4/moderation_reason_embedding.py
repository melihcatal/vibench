from __future__ import annotations

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-large"


def moderation_reason_embedding(reason_text: str) -> dict[str, object]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=reason_text)
    return {
        "provider": "openai",
        "model": EMBEDDING_MODEL,
        "embedding": response.data[0].embedding,
        "dimensions": len(response.data[0].embedding),
    }
