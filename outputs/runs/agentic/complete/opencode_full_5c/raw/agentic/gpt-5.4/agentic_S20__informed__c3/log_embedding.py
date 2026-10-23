from __future__ import annotations

from typing import List
import os

from openai import OpenAI


def log_embedding(
    messages: List[str], model: str = "text-embedding-3-large"
) -> List[List[float]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=model, input=messages)
    return [list(item.embedding) for item in response.data]
