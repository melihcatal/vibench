from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"



def translation_memory_embedding(segments: Iterable[str]) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    texts = [str(segment) for segment in segments]
    if not texts:
        raise ValueError("segments must not be empty")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]
