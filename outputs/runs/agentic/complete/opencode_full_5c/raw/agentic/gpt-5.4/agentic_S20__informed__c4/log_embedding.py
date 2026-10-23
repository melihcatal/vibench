from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI


def log_embedding(
    messages: Iterable[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=model, input=list(messages))
    return [item.embedding for item in response.data]
