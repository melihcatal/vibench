from __future__ import annotations

from typing import List

from openai import OpenAI


def embed_output(text: str, model: str = "text-embedding-3-small") -> List[float]:
    client = OpenAI()
    response = client.embeddings.create(model=model, input=text)
    return list(response.data[0].embedding)
