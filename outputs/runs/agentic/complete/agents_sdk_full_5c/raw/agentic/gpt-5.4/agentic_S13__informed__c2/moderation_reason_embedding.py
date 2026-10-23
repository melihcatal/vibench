from __future__ import annotations

import os
from typing import Dict, Iterable, List

from openai import OpenAI


def moderation_reason_embedding(
    rationales: Iterable[str],
    model: str = "text-embedding-3-small",
) -> Dict[str, object]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    inputs: List[str] = list(rationales)
    response = client.embeddings.create(model=model, input=inputs)
    return {
        "provider": "OpenAI Embeddings",
        "model": model,
        "vectors": [item.embedding for item in response.data],
        "count": len(response.data),
    }
