from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _text(value: Any) -> str:
    return "" if value is None else str(value)


def normalize_categories(raw: Any) -> Dict[str, float]:
    if isinstance(raw, dict):
        return {str(k): float(v) for k, v in raw.items() if v is not None}
    return {}


@dataclass
class SafetyTextRequest:
    text: str


@dataclass
class SafetyBatchRequest:
    messages: List[str]


@dataclass
class SafetyThresholdConfig:
    thresholds: Dict[str, float]


@dataclass
class SafetyModerationResult:
    flagged: bool
    categories: Dict[str, float]
    raw: Dict[str, Any]


@dataclass
class SafetyBatchResult:
    results: List[SafetyModerationResult]


def normalize_moderation_response(payload: Dict[str, Any]) -> SafetyModerationResult:
    results = payload.get("results") or payload.get("output") or []
    item = results[0] if results else payload
    return SafetyModerationResult(
        flagged=bool(item.get("flagged", False)),
        categories=normalize_categories(
            item.get("categories") or item.get("category_scores") or {}
        ),
        raw=payload,
    )


def normalize_batch_response(payload: Dict[str, Any]) -> SafetyBatchResult:
    items = payload.get("results") or payload.get("output") or []
    results = []
    for item in items:
        results.append(
            SafetyModerationResult(
                flagged=bool(item.get("flagged", False)),
                categories=normalize_categories(
                    item.get("categories") or item.get("category_scores") or {}
                ),
                raw=item,
            )
        )
    return SafetyBatchResult(results=results)
