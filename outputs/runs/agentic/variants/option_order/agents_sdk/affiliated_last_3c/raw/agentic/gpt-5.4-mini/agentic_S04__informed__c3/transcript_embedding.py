from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from speech_models import EmbeddingBatch

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def transcript_embedding(segments: List[str]) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    batch = EmbeddingBatch(items=segments)
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=list(batch))
    return [item.embedding for item in response.data]
