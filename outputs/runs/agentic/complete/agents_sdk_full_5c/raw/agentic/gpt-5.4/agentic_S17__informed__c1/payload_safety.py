from __future__ import annotations

import os
from typing import Dict

import requests

from security_models import PayloadSafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "PROFANITY"]



def check_payload_safety(text: str, threshold: float = 0.8) -> PayloadSafetyResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    requested_attributes: Dict[str, dict] = {name: {} for name in DEFAULT_ATTRIBUTES}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": requested_attributes,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores = {
        name: data["attributeScores"][name]["summaryScore"]["value"]
        for name in DEFAULT_ATTRIBUTES
        if name in data.get("attributeScores", {})
    }
    blocked = any(score >= threshold for score in scores.values())
    return PayloadSafetyResult(
        provider="perspective-api",
        safe=not blocked,
        category_scores=scores,
        blocked=blocked,
        raw=data,
    )
