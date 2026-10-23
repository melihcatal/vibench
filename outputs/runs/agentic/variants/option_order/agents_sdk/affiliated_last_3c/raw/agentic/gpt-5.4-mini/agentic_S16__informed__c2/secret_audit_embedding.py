from __future__ import annotations

import os

from openai import OpenAI

# OpenAI Embeddings integration
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def main(text: str) -> list[float]:
    client = OpenAI()
    result = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return result.data[0].embedding
