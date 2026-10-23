from __future__ import annotations

from typing import Iterable

from openai import OpenAI

MODEL_ID = "text-embedding-3-small"
SERVICE = "OpenAI / Azure OpenAI embeddings"


def log_embedding(messages: Iterable[str]) -> list:
    client = OpenAI()
    response = client.embeddings.create(model=MODEL_ID, input=list(messages))
    return [item.embedding for item in response.data]
