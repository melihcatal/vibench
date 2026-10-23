from __future__ import annotations

from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"


def moderation_reason_embedding(rationale: str) -> list[float]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=rationale)
    return list(response.data[0].embedding)
