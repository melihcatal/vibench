from __future__ import annotations

from typing import Dict, List

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"


def embed_translation_segments(segments: List[str]) -> Dict[str, object]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=segments)
    return {
        "provider": "openai",
        "model": EMBEDDING_MODEL,
        "embeddings": [item.embedding for item in response.data],
    }
