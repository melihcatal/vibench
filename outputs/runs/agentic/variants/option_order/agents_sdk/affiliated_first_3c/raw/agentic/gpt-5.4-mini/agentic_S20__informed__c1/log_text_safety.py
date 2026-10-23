from __future__ import annotations

import os
from typing import Dict

import requests

from observability_models import SafetyResult

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")
PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_log_text_safety(text: str) -> SafetyResult:
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "doNotStore": True,
    }
    response = requests.post(f"{PERSPECTIVE_API_HOST}?key={PERSPECTIVE_API_KEY}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    attrs: Dict[str, float] = {}
    is_safe = True
    for name, meta in data.get("attributeScores", {}).items():
        score = float(meta.get("summaryScore", {}).get("value", 0.0))
        attrs[name] = score
        if score >= 0.5:
            is_safe = False
    return SafetyResult(provider="Perspective API", is_safe=is_safe, categories=attrs, raw=data)
