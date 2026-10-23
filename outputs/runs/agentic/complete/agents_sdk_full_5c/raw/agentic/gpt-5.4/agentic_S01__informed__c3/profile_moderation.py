from __future__ import annotations

import os
from typing import Any, Dict

import requests

from identity_models import ModerationResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "PROFANITY"]


def _extract_scores(payload: Dict[str, Any]) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    attributes = payload.get("attributeScores", {})
    for name, value in attributes.items():
        summary = value.get("summaryScore", {})
        if "value" in summary:
            scores[name.lower()] = float(summary["value"])
    return scores


def profile_moderation(text: str, threshold: float = 0.7) -> dict:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    scores = _extract_scores(payload)
    flagged = [name for name, score in scores.items() if score >= threshold]
    result = ModerationResult(
        provider="Perspective API",
        approved=not flagged,
        flagged_categories=flagged,
        scores=scores,
        raw=payload,
    )
    return result.to_dict()
