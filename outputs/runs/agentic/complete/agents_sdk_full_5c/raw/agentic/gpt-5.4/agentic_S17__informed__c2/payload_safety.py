from __future__ import annotations

from typing import Dict

import requests

from security_client import get_perspective_api_key
from security_models import SafetyAssessment


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_payload_safety(text: str) -> SafetyAssessment:
    api_key = get_perspective_api_key()
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "PROFANITY": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores: Dict[str, float] = {
        name.lower(): details["summaryScore"]["value"]
        for name, details in data.get("attributeScores", {}).items()
    }
    unsafe = any(score >= 0.7 for score in scores.values())
    return SafetyAssessment(
        text=text,
        unsafe=unsafe,
        categories=scores,
        provider="perspective-api",
    )
