from __future__ import annotations

from typing import Any, Dict, Iterable, List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def translation_memory_embedding(segments: Iterable[str]) -> Dict[str, Any]:
    client = OpenAI()
    inputs: List[str] = [str(segment) for segment in segments]
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=inputs)
    return {
        "provider": "OpenAI",
        "model": OPENAI_EMBEDDING_MODEL,
        "embeddings": [item.embedding for item in response.data],
        "usage": getattr(response, "usage", None),
    }
