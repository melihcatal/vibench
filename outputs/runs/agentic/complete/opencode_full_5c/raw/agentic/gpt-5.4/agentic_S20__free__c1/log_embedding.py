from __future__ import annotations

import os

from openai import OpenAI


def log_embedding(messages: list[str], model: str = "text-embedding-3-small") -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=model, input=messages)
    return {
        "provider": "OpenAI",
        "model": model,
        "embeddings": [item.embedding for item in response.data],
    }
