from __future__ import annotations

import os
from typing import Any, Dict

import requests

from document_models import normalize_text


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_ocr_text_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: PERSPECTIVE_API_KEY")

    payload = {
        "comment": {"text": normalize_text(text)},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
        },
    }
    response = requests.post(f"{PERSPECTIVE_API_URL}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    scores = {
        name: value["summaryScore"]["value"]
        for name, value in data.get("attributeScores", {}).items()
    }
    return {"provider": "perspective-api", "scores": scores, "raw": data}
