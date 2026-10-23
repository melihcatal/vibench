from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


def check_corpus_safety(texts: list[str], model: str = "omni-moderation-latest") -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required.")
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(model=model, input=texts)
    payload = response.model_dump()
    flagged_count = sum(1 for item in payload.get("results", []) if item.get("flagged"))
    return {
        "provider": "OpenAI",
        "model": model,
        "flagged_count": flagged_count,
        "results": payload.get("results", []),
    }
