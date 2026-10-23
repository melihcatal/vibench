from __future__ import annotations

from typing import Dict

import requests

from messaging_models import SafetyResult


PERSPECTIVE_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def message_safety(text: str) -> SafetyResult:
    api_key = __import__("os").getenv("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
        "languages": ["en"],
    }
    response = requests.post(f"{PERSPECTIVE_HOST}?key={api_key}", json=payload, timeout=15)
    response.raise_for_status()
    data: Dict[str, object] = response.json()
    score = float(
        data.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )
    return SafetyResult(unsafe=score >= 0.5, score=score, provider="perspective-api", categories=data.get("attributeScores", {}))
