from __future__ import annotations

import os

from openai import OpenAI


def transcript_embedding(segments: list[str]) -> dict[str, object]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=segments,
    )
    return {
        "provider": "OpenAI",
        "model": "text-embedding-3-large",
        "embeddings": [item.embedding for item in response.data],
    }
