from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


def moderation_reason_embedding(reasons: Iterable[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    inputs = list(reasons)
    if not inputs:
        return []
    response = client.embeddings.create(model="text-embedding-3-large", input=inputs)
    return [item.embedding for item in response.data]
