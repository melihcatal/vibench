from __future__ import annotations

import os
import requests

from messaging_models import SafetyCheckResult, normalize_payload_text

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def message_safety(text: object) -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    payload_text = normalize_payload_text(text)
    if not api_key:
        return SafetyCheckResult(provider="Perspective API", unsafe=False, score=0.0, categories={"fallback": 0.0})
    body = {
        "comment": {"text": payload_text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    resp = requests.post(f"{PERSPECTIVE_API_URL}?key={api_key}", json=body, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return SafetyCheckResult(provider="Perspective API", unsafe=score >= 0.7, score=score, categories={"TOXICITY": score})
