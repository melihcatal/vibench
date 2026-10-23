from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


def embed_transcript_segments(segments: Iterable[str]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    inputs = list(segments)
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=inputs,
    )
    vectors: List[List[float]] = [item.embedding for item in response.data]
    return {
        "provider": "OpenAI",
        "model": "text-embedding-3-large",
        "embedding_count": len(vectors),
        "embeddings": vectors,
    }
