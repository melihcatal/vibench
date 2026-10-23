from __future__ import annotations

import os
from typing import List

from openai import OpenAI


def embed_translated_segments(segments: List[str]) -> list[list[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=segments,
    )
    return [item.embedding for item in response.data]
