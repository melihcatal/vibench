from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI


def embed_caption_chunks(chunks: Iterable[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    values = [chunk for chunk in chunks if chunk.strip()]
    if not values:
        return []
    response = client.embeddings.create(model="text-embedding-3-small", input=values)
    return [item.embedding for item in response.data]
