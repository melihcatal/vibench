from __future__ import annotations

import os
from typing import Dict

import requests

from security_models import SafetyCheckResult, normalize_text

PROVIDER = "perspective-api"
PERSPECTIVE_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_payload_safety(text: str, languages: str = "en") -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    payload: Dict[str, object] = {
        "comment": {"text": normalize_text(text)},
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        "languages": [languages],
    }
    response = requests.post(PERSPECTIVE_HOST, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    labels = {}
    score = 0.0
    for attr, details in data.get("attributeScores", {}).items():
        value = details.get("summaryScore", {}).get("value", 0.0)
        labels[attr] = float(value)
        score = max(score, float(value))
    unsafe = score >= float(os.getenv("MODERATION_THRESHOLD", "0.65"))
    return SafetyCheckResult(provider=PROVIDER, unsafe=unsafe, score=score, labels=labels, metadata=data)
