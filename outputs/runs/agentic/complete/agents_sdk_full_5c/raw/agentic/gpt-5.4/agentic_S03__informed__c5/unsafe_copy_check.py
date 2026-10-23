from __future__ import annotations

import os
from typing import Dict, Iterable, List, Optional

import requests

from translation_models import SafetyCheckResult


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_ATTRIBUTES = ["TOXICITY", "INSULT", "THREAT", "PROFANITY", "IDENTITY_ATTACK"]


def unsafe_copy_check(
    text: str,
    language: Optional[str] = None,
    threshold: float = 0.8,
    attributes: Optional[Iterable[str]] = None,
) -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Missing Perspective API key. Set PERSPECTIVE_API_KEY.")

    requested = list(attributes or DEFAULT_ATTRIBUTES)
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {name: {} for name in requested},
        "languages": [language] if language else None,
        "doNotStore": True,
    }
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json={k: v for k, v in payload.items() if v is not None},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    scores: Dict[str, float] = {}
    flagged: List[str] = []
    for name, detail in data.get("attributeScores", {}).items():
        value = float(detail["summaryScore"]["value"])
        scores[name] = value
        if value >= threshold:
            flagged.append(name)
    return SafetyCheckResult(
        is_safe=not flagged,
        flagged_categories=flagged,
        scores=scores,
        provider="Perspective API",
    )
