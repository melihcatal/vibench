from __future__ import annotations

import os
from typing import Any, Dict, List

import requests


VOYAGE_EMBEDDINGS_URL = "https://api.voyageai.com/v1/embeddings"
VOYAGE_MODEL = "voyage-3-large"


def embed_document_sections(
    sections: List[str], input_type: str = "document"
) -> Dict[str, Any]:
    api_key = os.getenv("VOYAGE_API_KEY")
    if not api_key:
        raise ValueError("VOYAGE_API_KEY is required")
    response = requests.post(
        VOYAGE_EMBEDDINGS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": VOYAGE_MODEL, "input": sections, "input_type": input_type},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    return {
        "model": body.get("model", VOYAGE_MODEL),
        "embeddings": [item["embedding"] for item in body.get("data", [])],
    }
