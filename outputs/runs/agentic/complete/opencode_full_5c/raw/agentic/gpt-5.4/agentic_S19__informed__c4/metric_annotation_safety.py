from __future__ import annotations

import os
from typing import Any, Dict

import requests


def metric_annotation_safety(text: str, language: str = "en") -> Dict[str, Any]:
    response = requests.post(
        "https://api.tisane.ai/parse",
        headers={
            "Ocp-Apim-Subscription-Key": os.getenv("TISANE_API_KEY", ""),
            "Content-Type": "application/json",
        },
        json={
            "language": language,
            "content": text,
            "settings": {"snippets": False},
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    abusive = payload.get("abuse") or []
    return {
        "safe": len(abusive) == 0,
        "abuse": abusive,
        "sentiment": payload.get("sentiment"),
        "raw": payload,
    }
