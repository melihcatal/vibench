from __future__ import annotations

from typing import Dict

import requests

from messaging_models import SafetyResult

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_safety(text: str, api_key: str) -> SafetyResult:
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    resp = requests.post(PERSPECTIVE_API_URL, params={"key": api_key}, json=payload, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    score = float(data["attributeScores"]["TOXICITY"]["summaryScore"]["value"])
    return SafetyResult(unsafe=score >= 0.7, score=score, categories={"TOXICITY": score}, raw=data)
