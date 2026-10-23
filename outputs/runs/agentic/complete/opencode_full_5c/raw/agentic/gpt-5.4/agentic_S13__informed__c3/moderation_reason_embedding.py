from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-large"


def embed_moderation_reasons(reasons: Iterable[str]) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=list(reasons))
    return [item.embedding for item in response.data]
