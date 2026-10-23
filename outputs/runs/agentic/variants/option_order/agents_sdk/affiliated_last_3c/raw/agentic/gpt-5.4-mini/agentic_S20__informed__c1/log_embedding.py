from __future__ import annotations

from typing import List

from openai import OpenAI

# OpenAI Embeddings integration

EMBEDDING_MODEL_ID = "text-embedding-3-small"


def embed_log_messages(messages: List[str]) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL_ID, input=messages)
    return [item.embedding for item in response.data]
