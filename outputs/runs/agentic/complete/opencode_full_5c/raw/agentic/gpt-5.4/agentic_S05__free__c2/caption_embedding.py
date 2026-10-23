from __future__ import annotations

import os
from collections.abc import Iterable

from openai import OpenAI


def embed_caption_chunks(chunks: Iterable[str]) -> dict[str, object]:
    inputs = [chunk.strip() for chunk in chunks if chunk.strip()]
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-small", input=inputs)
    return {
        "embeddings": [item.embedding for item in response.data],
        "provider": "OpenAI text-embedding-3-small",
        "dimensions": len(response.data[0].embedding) if response.data else 0,
    }
