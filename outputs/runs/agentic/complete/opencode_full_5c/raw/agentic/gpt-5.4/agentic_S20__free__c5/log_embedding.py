from __future__ import annotations

import os

from openai import OpenAI


def log_embedding(messages: list[str]) -> list[list[float]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-large", input=messages)
    return [item.embedding for item in response.data]
