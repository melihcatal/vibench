from __future__ import annotations

from openai import OpenAI

EMBEDDING_MODEL_ID = "text-embedding-3-small"


def log_embedding(texts: list[str]) -> list[list[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL_ID, input=texts)
    return [item.embedding for item in response.data]
