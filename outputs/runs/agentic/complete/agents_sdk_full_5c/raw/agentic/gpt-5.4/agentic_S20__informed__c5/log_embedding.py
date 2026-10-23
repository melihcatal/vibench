from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def log_embedding(messages: Iterable[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    inputs = list(messages)
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=inputs,
    )
    return [item.embedding for item in response.data]
