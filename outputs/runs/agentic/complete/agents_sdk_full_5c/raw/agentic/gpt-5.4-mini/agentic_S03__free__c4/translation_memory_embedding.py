"""Embed translated segments for translation-memory search using OpenAI embeddings."""

from __future__ import annotations

import os
from typing import List

from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=segments)
    return [item.embedding for item in response.data]


__all__ = ["embed_translated_segments", "EMBEDDING_MODEL"]
