from __future__ import annotations

import os
from collections.abc import Sequence

from openai import OpenAI

from speech_models import normalize_caption_chunk


def embed_caption_chunks(chunks: Sequence[str]) -> list[list[float]]:
    inputs = [
        normalize_caption_chunk(chunk)
        for chunk in chunks
        if normalize_caption_chunk(chunk)
    ]
    if not inputs:
        return []
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=inputs,
    )
    return [item.embedding for item in response.data]
