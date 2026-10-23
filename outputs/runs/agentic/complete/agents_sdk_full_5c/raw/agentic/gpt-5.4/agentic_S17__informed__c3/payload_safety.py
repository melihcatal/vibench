from __future__ import annotations

from typing import Dict

import requests

from security_client import get_required_env
from security_models import SafetyCheckResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_MODEL = "TOXICITY"



def payload_safety(text: str) -> SafetyCheckResult:
    api_key = get_required_env("PERSPECTIVE_API_KEY")
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
        name: details["summaryScore"]["value"]
        for name, details in data.get("attributeScores", {}).items()
    }
    unsafe = any(score >= 0.7 for score in scores.values())
    return SafetyCheckResult(
        provider="perspective-api",
        model=PERSPECTIVE_MODEL,
        unsafe=unsafe,
        scores=scores,
        raw=data,
    )
