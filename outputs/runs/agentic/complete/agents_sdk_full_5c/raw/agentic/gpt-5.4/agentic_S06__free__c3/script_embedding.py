from __future__ import annotations

import os

from openai import OpenAI

from speech_models import EmbeddingResult

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_script(text: str) -> EmbeddingResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    item = response.data[0]
    return EmbeddingResult(
        provider="openai",
        vector=item.embedding,
        model=OPENAI_EMBEDDING_MODEL,
    )
