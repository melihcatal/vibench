from __future__ import annotations

import os

from openai import OpenAI

from speech_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_script(text: str) -> EmbeddingResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    vector = response.data[0].embedding
    return EmbeddingResult(
        provider="OpenAI",
        model=OPENAI_EMBEDDING_MODEL,
        embedding=vector,
        dimensions=len(vector),
        raw=response.model_dump(),
    )
