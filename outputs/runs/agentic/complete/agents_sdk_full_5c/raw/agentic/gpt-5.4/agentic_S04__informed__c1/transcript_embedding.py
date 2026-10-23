from __future__ import annotations

import os
from typing import Dict, List, Sequence

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"


def transcript_embedding(segments: Sequence[str]) -> Dict[str, List[Dict[str, object]]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    cleaned = [segment.strip() for segment in segments if segment and segment.strip()]
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=cleaned)
    vectors: List[Dict[str, object]] = []
    for index, item in enumerate(response.data):
        vectors.append(
            {
                "index": index,
                "text": cleaned[index],
                "embedding": item.embedding,
            }
        )
    return {
        "provider": "OpenAI",
        "model": EMBEDDING_MODEL,
        "embeddings": vectors,
    }
