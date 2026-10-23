from __future__ import annotations

from typing import List

from openai import OpenAI


def moderation_reason_embedding(text: str) -> List[float]:
    client = OpenAI()
    resp = client.embeddings.create(model="text-embedding-3-small", input=text)
    return list(resp.data[0].embedding)
