from __future__ import annotations

import os
from typing import Sequence

import requests

from translation_models import SafetyCheckResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ("TOXICITY", "SEVERE_TOXICITY", "INSULT", "THREAT", "PROFANITY")


def check_localized_copy_unsafe(texts: Sequence[str], threshold: float = 0.7) -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    aggregate: dict[str, float] = {}
    flagged_segments: list[str] = []
    for text in texts:
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {name: {} for name in DEFAULT_ATTRIBUTES},
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
        segment_flagged = False
        for name, details in attribute_scores.items():
            score = float(details["summaryScore"]["value"])
            aggregate[name] = max(score, aggregate.get(name, 0.0))
            if score >= threshold:
                segment_flagged = True
        if segment_flagged:
            flagged_segments.append(text)
    return SafetyCheckResult(
        is_safe=not flagged_segments,
        categories=aggregate,
        flagged_segments=flagged_segments,
        provider="Perspective API",
        raw=aggregate,
    )
