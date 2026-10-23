from __future__ import annotations

import requests

from observability_models import SafetyResult


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def log_text_safety(text: str) -> SafetyResult:
    params = {"key": __import__("os").getenv("PERSPECTIVE_API_KEY", "")}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        "languages": ["en"],
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    categories = [name.lower() for name, item in scores.items() if item.get("summaryScore", {}).get("value", 0) >= 0.5]
    unsafe = bool(categories)
    return SafetyResult(text=text, unsafe=unsafe, categories=categories, raw=data)
