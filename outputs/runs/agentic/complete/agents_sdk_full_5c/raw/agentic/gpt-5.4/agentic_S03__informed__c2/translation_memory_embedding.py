from __future__ import annotations

import os
from typing import Sequence

from openai import OpenAI

from translation_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_translated_segments(segments: Sequence[str]) -> EmbeddingResult:
    if not segments:
        raise ValueError("segments must not be empty")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=list(segments),
    )
    vectors = [item.embedding for item in response.data]
    dimensions = len(vectors[0]) if vectors else 0
    return EmbeddingResult(
        vectors=vectors,
        provider="OpenAI",
        model=OPENAI_EMBEDDING_MODEL,
        dimensions=dimensions,
        raw=response,
    )
