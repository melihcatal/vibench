from __future__ import annotations

import os

import requests

from observability_models import SafetyCheckResult

PERSPECTIVE_API_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_log_text_safety(text: str) -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    params = {"key": api_key}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
    }
    response = requests.post(PERSPECTIVE_API_HOST, params=params, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    categories = []
    unsafe = False
    attr = data.get("attributeScores", {}) if isinstance(data, dict) else {}
    for name, score_block in attr.items():
        value = score_block.get("summaryScore", {}).get("value", 0)
        if value >= 0.5:
            unsafe = True
            categories.append(name.lower())
    return SafetyCheckResult(unsafe=unsafe, categories=categories, raw_response=data)
