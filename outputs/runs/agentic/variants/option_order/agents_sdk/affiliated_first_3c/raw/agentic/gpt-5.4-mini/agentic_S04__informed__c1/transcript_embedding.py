from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"


def transcript_embedding(segments: Iterable[str]) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=list(segments))
    return [item.embedding for item in response.data]
