from __future__ import annotations

import os

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-large"


def embed_script(text: str) -> list[float]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding
