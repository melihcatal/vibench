from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


DEFAULT_EMBED_MODEL = "text-embedding-3-large"


def moderation_reason_embedding(texts: Iterable[str], *, model: str = DEFAULT_EMBED_MODEL) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=list(texts))
    return [item.embedding for item in response.data]
