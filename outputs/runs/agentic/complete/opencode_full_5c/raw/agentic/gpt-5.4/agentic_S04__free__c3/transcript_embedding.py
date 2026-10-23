from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def transcript_embedding(segments: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    normalized_segments: List[Dict[str, Any]] = list(segments)
    inputs = [segment.get("text", "") for segment in normalized_segments]
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=inputs,
    )
    embedded_segments = []
    for segment, embedding in zip(normalized_segments, response.data):
        embedded_segments.append(
            {
                **segment,
                "embedding": embedding.embedding,
            }
        )
    return {
        "provider": "OpenAI",
        "model": OPENAI_EMBEDDING_MODEL,
        "segments": embedded_segments,
    }
