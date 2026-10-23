from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from translation_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_translation_segments(segments: list[str]) -> EmbeddingResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=segments)
    vectors = [item.embedding for item in response.data]
    return EmbeddingResult(provider="OpenAI Embeddings", vectors=vectors, metadata={"model": OPENAI_EMBEDDING_MODEL})
