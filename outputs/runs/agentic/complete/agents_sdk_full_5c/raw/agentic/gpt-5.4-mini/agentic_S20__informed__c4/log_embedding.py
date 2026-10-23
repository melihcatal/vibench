from __future__ import annotations

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"


def log_embedding(text: str) -> list[float]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return list(response.data[0].embedding)
