from __future__ import annotations

import os

import requests

from model_models import SafetyResult

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_prompt(prompt: str) -> SafetyResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    payload = {
        "comment": {"text": prompt},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    resp = requests.post(f"{PERSPECTIVE_API_URL}?key={api_key}", json=payload, timeout=30)
    data = resp.json()
    scores = data.get("attributeScores", {})
    categories = []
    top = 0.0
    for name, info in scores.items():
        score = info.get("summaryScore", {}).get("value", 0.0)
        top = max(top, float(score))
        if score >= 0.5:
            categories.append(name)
    return SafetyResult(flagged=top >= 0.5, score=top, categories=categories, raw=data)
