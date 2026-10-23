from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from translation_models import EmbeddingResult

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def translation_memory_embedding(segments: Iterable[str]) -> EmbeddingResult:
    inputs = [str(segment) for segment in segments]
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
    response = client.embeddings.create(model=model, input=inputs)
    return EmbeddingResult(
        embeddings=[item.embedding for item in response.data],
        model=response.model,
        provider="OpenAI",
        raw={
            "usage": response.usage.model_dump() if response.usage else None,
        },
    )
