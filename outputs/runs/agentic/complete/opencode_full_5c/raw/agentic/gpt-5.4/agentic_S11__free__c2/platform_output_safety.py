from __future__ import annotations

import os
from typing import Any, Dict

import requests


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def platform_output_safety(text: str) -> Dict[str, Any]:
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    result = body["results"][0]
    return {
        "safe": not result["flagged"],
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "result": result,
        "raw": body,
    }
