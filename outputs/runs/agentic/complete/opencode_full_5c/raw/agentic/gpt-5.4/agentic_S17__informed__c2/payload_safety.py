from __future__ import annotations

import os
from typing import Dict

import requests

from security_models import PayloadSafetyResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def payload_safety(text: str) -> Dict[str, object]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing PERSPECTIVE_API_KEY")
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "PROFANITY": {},
            },
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    attribute_scores = data.get("attributeScores", {})
    scores = {
        name.lower(): float(value["summaryScore"]["value"])
        for name, value in attribute_scores.items()
    }
    blocked = [name for name, score in scores.items() if score >= 0.7]
    result = PayloadSafetyResult(
        provider="google-perspective-api",
        is_safe=not blocked,
        blocked_categories=blocked,
        scores=scores,
        raw_response=data,
    )
    return result.to_dict()
