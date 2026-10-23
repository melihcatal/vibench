from __future__ import annotations

import os

from openai import OpenAI


MODEL_ID = "text-embedding-3-small"


def log_embedding(text: str) -> list[float]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=MODEL_ID, input=text)
    return response.data[0].embedding
