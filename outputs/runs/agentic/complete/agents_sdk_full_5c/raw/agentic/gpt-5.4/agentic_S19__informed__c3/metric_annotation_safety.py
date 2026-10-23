from __future__ import annotations

import os
from typing import Dict

import requests

from observability_models import SafetyCheckResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def metric_annotation_safety(text: str, threshold: float = 0.8) -> SafetyCheckResult:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
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
    payload = response.json()
    scores: Dict[str, float] = {}
    blocked = []
    for name, details in payload.get("attributeScores", {}).items():
        value = float(details["summaryScore"]["value"])
        scores[name.lower()] = value
        if value >= threshold:
            blocked.append(name.lower())
    return SafetyCheckResult(
        text=text,
        unsafe=bool(blocked),
        scores=scores,
        blocked_categories=blocked,
    )
