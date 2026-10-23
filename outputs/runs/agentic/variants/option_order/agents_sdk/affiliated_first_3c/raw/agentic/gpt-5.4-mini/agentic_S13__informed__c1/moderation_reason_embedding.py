from __future__ import annotations

from typing import List

from openai import OpenAI

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def moderation_reason_embedding(texts: List[str]) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]
