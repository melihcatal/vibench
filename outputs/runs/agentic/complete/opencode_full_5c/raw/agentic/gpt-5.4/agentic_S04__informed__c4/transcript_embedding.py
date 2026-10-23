from __future__ import annotations

import os

from openai import OpenAI


def transcript_embedding(segments: list[str]) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=segments,
    )
    return {
        "provider": "openai",
        "model": "text-embedding-3-large",
        "embeddings": [item.embedding for item in response.data],
    }
