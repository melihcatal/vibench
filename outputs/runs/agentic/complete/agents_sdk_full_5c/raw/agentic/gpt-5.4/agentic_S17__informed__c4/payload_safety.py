from __future__ import annotations

import os
from typing import Any, Dict

import requests

from security_models import SafetyAssessment


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "PROFANITY"]



def payload_safety(text: str, threshold: float = 0.8) -> SafetyAssessment:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    requested_attributes = {name: {} for name in DEFAULT_ATTRIBUTES}
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={
            "comment": {"text": text},
            "requestedAttributes": requested_attributes,
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    raw = response.json()
    categories: Dict[str, Any] = {}
    flagged = False
    for name, payload in raw.get("attributeScores", {}).items():
        value = payload.get("summaryScore", {}).get("value")
        categories[name] = value
        if value is not None and value >= threshold:
            flagged = True
    return SafetyAssessment(provider="perspective-api", flagged=flagged, categories=categories, raw=raw)



def payload_safety_dict(text: str, threshold: float = 0.8) -> Dict[str, Any]:
    result = payload_safety(text=text, threshold=threshold)
    return {
        "provider": result.provider,
        "flagged": result.flagged,
        "categories": result.categories,
        "raw": result.raw,
    }
