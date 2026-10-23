import os
from dataclasses import dataclass
from typing import List, Optional, Tuple

import requests


OPENAI_MODERATION_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


@dataclass
class UnsafeSpan:
    start: int
    end: int
    label: str
    score: float


def _modereration_request(text: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _flagged_categories(result: dict) -> List[Tuple[str, float]]:
    categories = result.get("categories", {}) or {}
    scores = result.get("category_scores", {}) or {}
    flagged = []
    for category, is_flagged in categories.items():
        if is_flagged:
            flagged.append((category, float(scores.get(category, 1.0))))
    return sorted(flagged, key=lambda item: item[1], reverse=True)


def redact_unsafe(text: str, redact_token: str = "[REDACTED]") -> Tuple[str, List[UnsafeSpan]]:
    payload = _modereration_request(text)
    results = payload.get("results", [])
    if not results:
        return text, []
    result = results[0]
    flagged = _flagged_categories(result)
    if not flagged:
        return text, []
    spans: List[UnsafeSpan] = []
    unsafe = result.get("flagged", False)
    if unsafe:
        spans.append(UnsafeSpan(start=0, end=len(text), label=flagged[0][0], score=flagged[0][1]))
        return redact_token, spans
    return text, []


def flags_or_redacts_unsafe_spans(text: str, redact: bool = True) -> Tuple[str, List[UnsafeSpan]]:
    redacted, spans = redact_unsafe(text)
    if not redact:
        return text, spans
    return redacted, spans
