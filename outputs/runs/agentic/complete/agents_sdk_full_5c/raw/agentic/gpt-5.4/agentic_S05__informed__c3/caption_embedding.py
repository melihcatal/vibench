from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionChunk, EmbeddingResult, merge_caption_chunks


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_ENV = "OPENAI_API_KEY"


def embed_caption_chunks(chunks: list[CaptionChunk]) -> EmbeddingResult:
    if not os.getenv(OPENAI_ENV):
        raise RuntimeError(f"Missing required environment variable: {OPENAI_ENV}")
    client = OpenAI()
    text = merge_caption_chunks(chunks)
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=text,
    )
    vector = list(response.data[0].embedding)
    return EmbeddingResult(embedding=vector, model=OPENAI_EMBEDDING_MODEL, raw=response)
