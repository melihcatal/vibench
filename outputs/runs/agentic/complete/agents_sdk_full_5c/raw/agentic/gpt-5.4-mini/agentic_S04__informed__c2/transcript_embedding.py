from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"


def transcript_embedding(segments: List[str]) -> Dict[str, Any]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=segments)
    vectors = [item.embedding for item in response.data]
    return {"provider": "OpenAI", "model": EMBEDDING_MODEL, "embeddings": vectors}
