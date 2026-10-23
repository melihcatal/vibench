from __future__ import annotations

import os
from typing import Any, Dict

import requests


def platform_output_embedding(text: str) -> Dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "text-embedding-3-large",
            "input": text,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    item = data["data"][0]
    return {
        "embedding": item.get("embedding", []),
        "index": item.get("index", 0),
        "model": data.get("model", "text-embedding-3-large"),
        "usage": data.get("usage", {}),
        "raw_response": data,
    }
