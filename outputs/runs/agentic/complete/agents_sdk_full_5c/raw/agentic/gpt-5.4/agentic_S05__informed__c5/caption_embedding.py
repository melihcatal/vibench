from __future__ import annotations

import os

from openai import OpenAI

from speech_models import EmbeddingResult, normalize_text


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_caption_chunk(text: str) -> EmbeddingResult:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {OPENAI_API_KEY_ENV}")

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=normalize_text(text),
    )
    vector = list(response.data[0].embedding)
    return EmbeddingResult(vector=vector, model=OPENAI_EMBEDDING_MODEL, raw=response)
