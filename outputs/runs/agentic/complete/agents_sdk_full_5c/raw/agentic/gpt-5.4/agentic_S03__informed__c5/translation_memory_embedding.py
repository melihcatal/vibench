from __future__ import annotations

import os
from typing import List, Sequence

from openai import OpenAI

from translation_models import EmbeddingResult, coerce_text_list


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_translated_segments(segments: Sequence[str]) -> EmbeddingResult:
    texts = coerce_text_list(segments)
    if not texts:
        raise ValueError("At least one segment is required.")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=texts,
    )
    vectors: List[List[float]] = [list(item.embedding) for item in response.data]
    return EmbeddingResult(
        vectors=vectors,
        model=OPENAI_EMBEDDING_MODEL,
        provider="OpenAI",
    )
