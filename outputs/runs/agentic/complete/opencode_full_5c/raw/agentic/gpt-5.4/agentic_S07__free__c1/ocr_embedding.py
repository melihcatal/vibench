from __future__ import annotations

import os
from typing import Any, Dict, List

import requests

from document_models import normalize_sections


def embed_document_sections(text: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: OPENAI_API_KEY")
    sections = normalize_sections(text)
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": "text-embedding-3-large", "input": sections},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    vectors: List[List[float]] = [item["embedding"] for item in payload.get("data", [])]
    return {
        "provider": "openai",
        "model": "text-embedding-3-large",
        "sections": sections,
        "vectors": vectors,
    }
