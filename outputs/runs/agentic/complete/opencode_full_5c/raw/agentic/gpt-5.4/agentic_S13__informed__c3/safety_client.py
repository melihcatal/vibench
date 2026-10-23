from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

import requests

from safety_models import (
    CategoryScore,
    SafetyRequest,
    SafetyResult,
    normalize_perspective_scores,
)


PERSPECTIVE_API_HOST = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)
PERSPECTIVE_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "IDENTITY_ATTACK",
]


def get_perspective_api_key() -> str:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise ValueError("Missing PERSPECTIVE_API_KEY")
    return api_key


def perspective_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def build_perspective_payload(request: SafetyRequest) -> Dict[str, Any]:
    return {
        "comment": {"text": request.text},
        "languages": [request.language],
        "requestedAttributes": {name: {} for name in PERSPECTIVE_ATTRIBUTES},
        "doNotStore": True,
    }


def analyze_text(request: SafetyRequest, timeout: float = 20.0) -> SafetyResult:
    api_key = get_perspective_api_key()
    response = requests.post(
        PERSPECTIVE_API_HOST,
        params={"key": api_key},
        headers=perspective_headers(),
        json=build_perspective_payload(request),
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    categories = normalize_perspective_scores(payload)
    flagged = any(score.score >= 0.5 for score in categories)
    return SafetyResult(
        text=request.text,
        allow=not flagged,
        flagged=flagged,
        categories=categories,
        provider="Perspective API",
        model="commentanalyzer-v1alpha1",
        raw=payload,
    )


def analyze_batch(
    requests_: Iterable[SafetyRequest], timeout: float = 20.0
) -> List[SafetyResult]:
    return [analyze_text(item, timeout=timeout) for item in requests_]


def highest_category(categories: List[CategoryScore]) -> CategoryScore | None:
    if not categories:
        return None
    return max(categories, key=lambda item: item.score)
