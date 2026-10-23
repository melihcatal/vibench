from __future__ import annotations

import os
from typing import Any, Dict

import requests


COHERE_EMBED_MODEL = os.getenv("COHERE_EMBED_MODEL", "embed-english-v3.0")


def platform_output_embedding(
    text: str, input_type: str = "search_document"
) -> Dict[str, Any]:
    response = requests.post(
        "https://api.cohere.com/v1/embed",
        headers={
            "Authorization": f"Bearer {os.environ['COHERE_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": COHERE_EMBED_MODEL,
            "texts": [text],
            "input_type": input_type,
            "embedding_types": ["float"],
        },
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    return {
        "embedding": body["embeddings"]["float"][0],
        "model": COHERE_EMBED_MODEL,
        "provider": "cohere",
        "raw": body,
    }
