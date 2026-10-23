from __future__ import annotations

import os

import requests

from embeddings_models import normalize_texts


def corpus_safety(texts: list[str]) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    normalized = normalize_texts(texts)
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": "omni-moderation-latest", "input": normalized},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results", [])
    return {
        "provider": "OpenAI",
        "model": "omni-moderation-latest",
        "approved": all(not item.get("flagged", False) for item in results),
        "results": results,
    }
