from __future__ import annotations

from typing import Dict

import requests

from security_client import get_perspective_headers
from security_models import SafetyCheck


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_secret_label_safety(text: str) -> SafetyCheck:
    response = requests.post(
        PERSPECTIVE_API_URL,
        headers=get_perspective_headers(),
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}},
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores: Dict[str, float] = {
        name.lower(): details["summaryScore"]["value"]
        for name, details in payload.get("attributeScores", {}).items()
    }
    max_score = max(scores.values(), default=0.0)
    return SafetyCheck(
        text=text, flagged=max_score >= 0.7, score=max_score, categories=scores
    )
