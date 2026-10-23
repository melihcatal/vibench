from __future__ import annotations

from typing import List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_script(text: str, api_key: str) -> List[float]:
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    return response.data[0].embedding
