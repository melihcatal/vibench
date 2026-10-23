from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


def embed_caption_chunks(chunks: Iterable[str]) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    inputs = [chunk for chunk in chunks if chunk.strip()]
    if not inputs:
        return []
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model="text-embedding-3-small", input=inputs)
    return [item.embedding for item in response.data]
