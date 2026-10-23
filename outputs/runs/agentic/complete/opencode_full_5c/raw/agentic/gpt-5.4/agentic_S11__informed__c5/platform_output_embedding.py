from __future__ import annotations

import os

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-large"


def platform_output_embedding(text: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    item = response.data[0]
    return {
        "provider": "OpenAI",
        "model": response.model,
        "embedding": item.embedding,
        "dimensions": len(item.embedding),
    }
