from __future__ import annotations

import requests

from identity_client import get_perspective_settings
from identity_models import ModerationResult


DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "INSULT",
    "PROFANITY",
    "THREAT",
]


def profile_moderation(text: str, threshold: float = 0.7) -> ModerationResult:
    settings = get_perspective_settings()
    requested_attributes = {name: {} for name in DEFAULT_ATTRIBUTES}
    response = requests.post(
        settings["api_url"],
        params={"key": settings["api_key"]},
        json={
            "comment": {"text": text},
            "requestedAttributes": requested_attributes,
            "languages": ["en"],
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json().get("attributeScores", {})
    scores = {
        name.lower(): float(value["summaryScore"]["value"])
        for name, value in data.items()
    }
    flagged_categories = [name for name, score in scores.items() if score >= threshold]
    flagged = bool(flagged_categories)
    return ModerationResult(
        provider="perspectiveapi",
        flagged=flagged,
        scores=scores,
        allowed=not flagged,
        flagged_categories=flagged_categories,
    )
