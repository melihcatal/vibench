from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


def normalize_severity(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        mapping = {"safe": 0, "low": 1, "medium": 2, "high": 3, "very_high": 4}
        if normalized in mapping:
            return mapping[normalized]
        try:
            return int(float(normalized))
        except ValueError:
            return 0
    return 0


def normalize_category_scores(scores: Optional[Mapping[str, Any]]) -> Dict[str, int]:
    if not scores:
        return {}
    normalized: Dict[str, int] = {}
    for category, value in scores.items():
        if isinstance(value, Mapping):
            for key in ("severity", "level", "score"):
                if key in value:
                    normalized[category] = normalize_severity(value[key])
                    break
            else:
                normalized[category] = 0
        else:
            normalized[category] = normalize_severity(value)
    return normalized


def normalize_categories(categories: Optional[Mapping[str, Any]]) -> Dict[str, bool]:
    if not categories:
        return {}
    normalized: Dict[str, bool] = {}
    for category, value in categories.items():
        if isinstance(value, bool):
            normalized[category] = value
        elif isinstance(value, (int, float)):
            normalized[category] = bool(value)
        elif isinstance(value, str):
            normalized[category] = value.strip().lower() in {"true", "1", "yes", "y", "flagged"}
        else:
            normalized[category] = bool(value)
    return normalized


@dataclass(frozen=True)
class SafetyRequest:
    text: str
    model: Optional[str] = None
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": self.text}
        if self.model:
            payload["model"] = self.model
        if self.user_id:
            payload["user_id"] = self.user_id
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class SafetyResponse:
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, int]
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api_response(cls, data: Mapping[str, Any]) -> "SafetyResponse":
        results = data.get("results") if isinstance(data, Mapping) else None
        if isinstance(results, list) and results:
            result = results[0]
            if isinstance(result, Mapping):
                return cls(
                    flagged=bool(result.get("flagged", False)),
                    categories=normalize_categories(result.get("categories")),
                    category_scores=normalize_category_scores(result.get("category_scores")),
                    raw=dict(data),
                )
        return cls(flagged=False, categories={}, category_scores={}, raw=dict(data))


def normalize_moderation_result(result: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "flagged": bool(result.get("flagged", False)),
        "categories": normalize_categories(result.get("categories")),
        "category_scores": normalize_category_scores(result.get("category_scores")),
        "raw": dict(result),
    }


def response_from_result(result: Mapping[str, Any]) -> SafetyResponse:
    return SafetyResponse(
        flagged=bool(result.get("flagged", False)),
        categories=normalize_categories(result.get("categories")),
        category_scores=normalize_category_scores(result.get("category_scores")),
        raw=dict(result),
    )
