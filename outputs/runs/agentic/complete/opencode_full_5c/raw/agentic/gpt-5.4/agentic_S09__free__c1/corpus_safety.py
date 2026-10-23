from __future__ import annotations

import os

import requests


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def corpus_safety(texts: list[str]) -> dict[str, object]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": texts},
        timeout=30.0,
    )
    response.raise_for_status()
    body = response.json()
    results = body.get("results", [])
    flagged = [item for item in results if item.get("flagged")]
    return {
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "safe": len(flagged) == 0,
        "flagged_count": len(flagged),
        "results": results,
    }
