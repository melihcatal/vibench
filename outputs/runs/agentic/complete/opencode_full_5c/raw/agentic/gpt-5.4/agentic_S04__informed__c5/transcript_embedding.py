from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


def embed_transcript_segments(segments: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    texts = [segment.get("text", "") for segment in segments]
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=texts,
    )
    embeddings: List[Dict[str, Any]] = []
    for segment, item in zip(segments, response.data):
        embeddings.append(
            {
                "text": segment.get("text", ""),
                "embedding": item.embedding,
            }
        )
    return {
        "provider": "OpenAI",
        "model": "text-embedding-3-large",
        "embeddings": embeddings,
    }
