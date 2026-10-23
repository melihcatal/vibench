from __future__ import annotations

import os
from typing import Sequence

from openai import OpenAI

from translation_models import EmbeddingResult


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def translation_memory_embedding(segments: Sequence[str]) -> list[EmbeddingResult]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=DEFAULT_EMBEDDING_MODEL, input=list(segments))
    return [
        EmbeddingResult(
            embedding=item.embedding,
            dimensions=len(item.embedding),
            provider="openai",
            model=DEFAULT_EMBEDDING_MODEL,
            raw=item,
        )
        for item in response.data
    ]
