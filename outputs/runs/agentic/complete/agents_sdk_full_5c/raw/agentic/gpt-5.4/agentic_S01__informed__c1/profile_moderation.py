from __future__ import annotations

import os
from typing import Any, Dict

import requests

from identity_models import ModerationResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_THRESHOLD = 0.75


_ATTRIBUTE_MAP = {
    "TOXICITY": "toxicity",
    "SEVERE_TOXICITY": "severe_toxicity",
    "INSULT": "insult",
    "PROFANITY": "profanity",
    "THREAT": "threat",
    "IDENTITY_ATTACK": "identity_attack",
}


def profile_moderation(text: str, threshold: float = DEFAULT_THRESHOLD) -> Dict[str, Any]:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {key: {} for key in _ATTRIBUTE_MAP},
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    attribute_scores = data.get("attributeScores", {})

    scores = {}
    flagged = []
    for api_name, normalized_name in _ATTRIBUTE_MAP.items():
        value = attribute_scores.get(api_name, {}).get("summaryScore", {}).get("value", 0.0)
        score = float(value)
        scores[normalized_name] = score
        if score >= threshold:
            flagged.append(normalized_name)

    result = ModerationResult(
        allowed=not flagged,
        flagged_categories=flagged,
        scores=scores,
        provider="Perspective API",
    )
    return {
        "allowed": result.allowed,
        "flagged_categories": result.flagged_categories,
        "scores": result.scores,
        "provider": result.provider,
    }
