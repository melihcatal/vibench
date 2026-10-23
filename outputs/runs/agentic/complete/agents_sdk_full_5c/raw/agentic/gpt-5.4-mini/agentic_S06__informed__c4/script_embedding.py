from __future__ import annotations

from typing import List

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-large"


def embed_script(text: str) -> List[float]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return list(response.data[0].embedding)
