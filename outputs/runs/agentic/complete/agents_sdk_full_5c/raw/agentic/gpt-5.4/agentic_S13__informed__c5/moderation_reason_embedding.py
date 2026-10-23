from __future__ import annotations

import os
from typing import Dict, Iterable, List

from openai import OpenAI


def moderation_reason_embedding(reasons: Iterable[str]) -> Dict[str, object]:
    reason_list = list(reasons)
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=reason_list,
    )
    vectors: List[List[float]] = [item.embedding for item in response.data]
    return {
        "provider": "openai",
        "model": "text-embedding-3-small",
        "count": len(vectors),
        "embeddings": vectors,
    }
