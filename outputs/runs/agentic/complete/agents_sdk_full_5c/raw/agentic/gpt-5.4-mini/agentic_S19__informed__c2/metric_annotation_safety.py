from __future__ import annotations

from typing import Dict

import requests

from observability_models import SafetyResult


PERSPECTIVE_PROVIDER_SIGNAL = "commentanalyzer.googleapis.com"


def metric_annotation_safety(text: str) -> SafetyResult:
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {"comment": {"text": text}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}}}
    response = requests.post(url, json=payload, params={"key": "${PERSPECTIVE_API_KEY}"}, timeout=30)
    data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
    score = data.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    unsafe = bool(score and score >= 0.5)
    return SafetyResult(text=text, provider="Perspective API", unsafe=unsafe, labels={"toxicity": float(score or 0.0)}, raw=data)
