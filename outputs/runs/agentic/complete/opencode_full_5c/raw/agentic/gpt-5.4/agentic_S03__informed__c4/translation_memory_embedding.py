from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_translated_segments(segments: Iterable[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    values = [str(segment) for segment in segments]
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=values)
    return [item.embedding for item in response.data]
