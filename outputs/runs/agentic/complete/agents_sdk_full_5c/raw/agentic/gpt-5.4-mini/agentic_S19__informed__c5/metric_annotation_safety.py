from __future__ import annotations

import os

import requests

from observability_models import SafetyVerdict

PROVIDER = "Perspective API"
PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com"


def metric_annotation_safety(text: str) -> SafetyVerdict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    endpoint = f"{PERSPECTIVE_API_HOST}/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "doNotStore": True,
    }
    response = requests.post(endpoint, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    score = data.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value")
    return SafetyVerdict(provider=PROVIDER, is_safe=(score is None or float(score) < 0.5), score=score, reasons=[])
