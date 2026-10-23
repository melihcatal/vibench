from __future__ import annotations

from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_script(text: str) -> list[float]:
    client = OpenAI()
    response = client.embeddings.create(model=DEFAULT_EMBEDDING_MODEL, input=text)
    return response.data[0].embedding
