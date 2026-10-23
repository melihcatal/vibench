from __future__ import annotations

from typing import Dict, Optional

from openai import OpenAI

from model_client import DEFAULT_SAFETY_MODEL, get_client


def platform_output_safety(text: str, client: Optional[OpenAI] = None) -> Dict[str, object]:
    client = client or get_client()
    result = client.moderations.create(model=DEFAULT_SAFETY_MODEL, input=text)
    return {
        "provider": "openai",
        "model": DEFAULT_SAFETY_MODEL,
        "flagged": result.results[0].flagged if result.results else False,
        "categories": result.results[0].categories if result.results else {},
        "raw": result,
    }
