from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def log_embedding(messages: Iterable[str]) -> List[list[float]]:
    client = OpenAI()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=list(messages),
    )
    return [item.embedding for item in response.data]
