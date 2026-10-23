from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


@dataclass(frozen=True)
class ThresholdDecision:
    allow: bool
    flagged: bool
    triggered_categories: Dict[str, float]
    category_scores: Dict[str, float]
    raw: Dict[str, Any]


def _resolve_api_key(api_key: Optional[str]) -> str:
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")
    return token


def _openai_moderate(text: str, api_key: Optional[str] = None, model: str = OPENAI_MODERATION_MODEL) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {_resolve_api_key(api_key)}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _extract_result(payload: Dict[str, Any]) -> Dict[str, Any]:
    results = payload.get("results") or []
    return results[0] if results else {}


def _normalize_thresholds(thresholds: Optional[Mapping[str, float]]) -> Dict[str, float]:
    if not thresholds:
        return {}
    return {str(category): float(value) for category, value in thresholds.items()}


def apply_category_thresholds(
    text: str,
    thresholds: Optional[Mapping[str, float]] = None,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> ThresholdDecision:
    payload = _openai_moderate(text, api_key=api_key, model=model)
    result = _extract_result(payload)
    categories = {str(k): bool(v) for k, v in (result.get("categories") or {}).items()}
    scores = {str(k): float(v) for k, v in (result.get("category_scores") or {}).items()}
    normalized_thresholds = _normalize_thresholds(thresholds)

    triggered: Dict[str, float] = {}
    for category, threshold in normalized_thresholds.items():
        score = scores.get(category, 0.0)
        if score >= threshold:
            triggered[category] = score

    flagged = bool(result.get("flagged", False)) or any(categories.values()) or bool(triggered)
    allow = not flagged
    return ThresholdDecision(
        allow=allow,
        flagged=flagged,
        triggered_categories=triggered,
        category_scores=scores,
        raw=payload,
    )


def safety_threshold(text: str, thresholds: Optional[Mapping[str, float]] = None) -> bool:
    return apply_category_thresholds(text, thresholds=thresholds).allow


def safety_threshold_from_env(text: str) -> bool:
    return safety_threshold(text)
