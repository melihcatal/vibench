from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


def create_embedding_client(api_key: str | None = None) -> OpenAI:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=key)


def embed_caption_chunks(chunks: Iterable[str]) -> List[List[float]]:
    client = create_embedding_client()
    inputs = [chunk for chunk in chunks if chunk.strip()]
    if not inputs:
        return []
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=inputs,
    )
    return [item.embedding for item in response.data]
