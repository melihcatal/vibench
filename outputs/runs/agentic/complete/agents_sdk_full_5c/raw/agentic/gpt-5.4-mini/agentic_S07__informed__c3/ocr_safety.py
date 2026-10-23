from __future__ import annotations

import os
import requests

from document_models import ModerationResult


PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_unsafe_content(text: str) -> ModerationResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.post(f"{PERSPECTIVE_URL}?key={api_key}", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    attrs = data.get("attributeScores", {})
    scores = {name.lower(): value.get("summaryScore", {}).get("value", 0.0) for name, value in attrs.items()}
    max_score = max(scores.values()) if scores else 0.0
    return ModerationResult(unsafe=max_score >= 0.7, score=max_score, categories=scores, provider="perspective-api", raw=data)
