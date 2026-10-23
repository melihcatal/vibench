from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from translation_models import EmbeddingResult


def embed_translation_segment(segment: str) -> EmbeddingResult:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=segment)
    vector = response.data[0].embedding
    return EmbeddingResult(
        vector=vector,
        provider="openai",
        model="text-embedding-3-small",
        dimensions=len(vector),
        metadata={"input_length": len(segment)},
    )
