from __future__ import annotations

from typing import List

from openai import OpenAI

from model_models import EmbeddingResult


EMBEDDING_MODEL = "text-embedding-3-small"


def embed_platform_output(text: str) -> EmbeddingResult:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    vector: List[float] = list(response.data[0].embedding)
    return EmbeddingResult(text=text, vector=vector, provider="openai", raw=response)
