from __future__ import annotations

import os
import requests

from observability_models import SafetyCheckResult

PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def metric_annotation_safety(text: str, languages: list[str] | None = None) -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
    }
    if languages:
        payload["languages"] = languages
    response = requests.post(f"{PERSPECTIVE_API_ENDPOINT}?key={api_key}", json=payload, timeout=15)
    response.raise_for_status()
    data = response.json()
    categories = {k.lower(): v.get("summaryScore", {}).get("value", 0.0) for k, v in data.get("attributeScores", {}).items()}
    score = max(categories.values()) if categories else 0.0
    return SafetyCheckResult(text=text, safe=score < 0.5, score=score, categories=categories)
