from __future__ import annotations

from typing import List

from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"


def embed_moderation_reason(reason: str) -> List[float]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=reason)
    return list(response.data[0].embedding)
