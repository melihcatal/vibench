from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

import requests


OPENAI_MODERATION_API = "https://api.openai.com/v1/moderations"


@dataclass(frozen=True)
class UnsafeSpan:
    start: int
    end: int
    label: str
    score: float


@dataclass(frozen=True)
class RedactionResult:
    text: str
    spans: List[UnsafeSpan]
    flagged: bool


def _openai_headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _moderate_with_openai(text: str) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_MODERATION_API,
        headers=_openai_headers(),
        json={"model": "omni-moderation-latest", "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _extract_categories(payload: Dict[str, Any]) -> Dict[str, bool]:
    results = payload.get("results") or []
    if not results:
        return {}
    categories = results[0].get("categories") or {}
    return {str(k): bool(v) for k, v in categories.items()}


def _extract_scores(payload: Dict[str, Any]) -> Dict[str, float]:
    results = payload.get("results") or []
    if not results:
        return {}
    scores = results[0].get("category_scores") or {}
    return {str(k): float(v) for k, v in scores.items()}


def redact_unsafe(text: str, redact_char: str = "█") -> RedactionResult:
    payload = _moderate_with_openai(text)
    categories = _extract_categories(payload)
    scores = _extract_scores(payload)
    spans: List[UnsafeSpan] = []

    if any(categories.values()):
        spans.append(
            UnsafeSpan(
                start=0,
                end=len(text),
                label=next((k for k, v in categories.items() if v), "unsafe"),
                score=max(scores.values()) if scores else 1.0,
            )
        )

    if not spans:
        return RedactionResult(text=text, spans=[], flagged=False)

    redacted = redact_char * len(text)
    return RedactionResult(text=redacted, spans=spans, flagged=True)


def flag_unsafe(text: str) -> bool:
    return redact_unsafe(text).flagged
