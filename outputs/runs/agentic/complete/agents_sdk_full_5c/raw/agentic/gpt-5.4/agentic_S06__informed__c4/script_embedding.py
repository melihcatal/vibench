from __future__ import annotations

import os

from openai import OpenAI

from speech_models import EmbeddingResult, ensure_text


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_script(text: str) -> EmbeddingResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required for OpenAI embeddings")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=ensure_text(text, "text"),
    )
    vector = list(response.data[0].embedding)
    return EmbeddingResult(
        provider="openai",
        model=OPENAI_EMBEDDING_MODEL,
        vector=vector,
        dimensions=len(vector),
    )
