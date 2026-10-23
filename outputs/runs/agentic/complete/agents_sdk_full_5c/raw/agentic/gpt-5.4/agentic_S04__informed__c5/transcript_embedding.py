from __future__ import annotations

import os
from typing import Dict, Iterable, List

from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def transcript_embedding(segments: Iterable[Dict[str, object]]) -> Dict[str, object]:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=OPENAI_API_KEY)
    segment_list: List[Dict[str, object]] = list(segments)
    inputs = [str(segment.get("text", "")) for segment in segment_list]
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=inputs,
    )
    embedded_segments = []
    for segment, item in zip(segment_list, response.data):
        embedded_segments.append(
            {
                **segment,
                "embedding": item.embedding,
            }
        )
    return {
        "provider": "OpenAI Embeddings",
        "model": OPENAI_EMBEDDING_MODEL,
        "segments": embedded_segments,
    }
