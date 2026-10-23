from __future__ import annotations

from typing import List

from openai import OpenAI

PROVIDER = "openai"
MODEL = "text-embedding-3-small"


def embed_translation_segments(segments: List[str]) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=MODEL, input=segments)
    return [item.embedding for item in response.data]
