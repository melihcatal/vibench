from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from observability_models import EmbeddingResult

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_log_messages(messages: Iterable[str]) -> EmbeddingResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=list(messages))
    vectors: List[List[float]] = [item.embedding for item in response.data]
    return EmbeddingResult(provider="OpenAI", vectors=vectors, raw=response)
