from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from speech_models import CaptionChunk, EmbeddingResult, merge_caption_chunks


def embed_caption_chunks(chunks: Iterable[CaptionChunk], api_key: str | None = None) -> EmbeddingResult:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    text = merge_caption_chunks(chunks)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    item = response.data[0]
    return EmbeddingResult(vector=item.embedding, model="text-embedding-3-small", raw=response.model_dump())
