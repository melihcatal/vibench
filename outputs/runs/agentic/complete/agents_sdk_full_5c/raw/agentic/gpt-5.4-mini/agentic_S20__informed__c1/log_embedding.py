from __future__ import annotations

from openai import OpenAI


def log_embedding(messages: list[str]) -> list[list[float]]:
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=messages,
    )
    return [item.embedding for item in response.data]
