from __future__ import annotations

import os

from openai import OpenAI


def embed_script(text: str) -> list[float]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI embeddings")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return list(response.data[0].embedding)
