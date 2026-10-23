from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Union


def _coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _coerce_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "y", "on"}:
            return True
        if lowered in {"false", "0", "no", "n", "off"}:
            return False
    return bool(value)


def _coerce_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _normalize_category_scores(value: Any) -> Dict[str, float]:
    if not isinstance(value, Mapping):
        return {}
    return {str(k): _coerce_float(v) for k, v in value.items()}


@dataclass
class SafetyRequest:
    text: str
    language: Optional[str] = None
    categories: List[str] = field(default_factory=list)
    include_rationales: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SafetyRequest":
        return cls(
            text=_coerce_str(data.get("text")),
            language=_coerce_str(data.get("language")) or None,
            categories=[str(item) for item in _coerce_list(data.get("categories")) if item is not None],
            include_rationales=_coerce_bool(data.get("include_rationales")),
            metadata=dict(data.get("metadata") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "text": self.text,
            "categories": list(self.categories),
            "include_rationales": self.include_rationales,
            "metadata": dict(self.metadata),
        }
        if self.language is not None:
            payload["language"] = self.language
        return payload


@dataclass
class SafetyCategoryResult:
    category: str
    score: float = 0.0
    flagged: bool = False
    rationale: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SafetyCategoryResult":
        return cls(
            category=_coerce_str(data.get("category")),
            score=_coerce_float(data.get("score")),
            flagged=_coerce_bool(data.get("flagged")),
            rationale=_coerce_str(data.get("rationale")) or None,
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "category": self.category,
            "score": self.score,
            "flagged": self.flagged,
        }
        if self.rationale is not None:
            payload["rationale"] = self.rationale
        return payload


@dataclass
class SafetyResponse:
    flagged: bool = False
    categories: List[SafetyCategoryResult] = field(default_factory=list)
    category_scores: Dict[str, float] = field(default_factory=dict)
    rationale: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SafetyResponse":
        categories_raw = _coerce_list(data.get("categories"))
        categories: List[SafetyCategoryResult] = []
        for item in categories_raw:
            if isinstance(item, Mapping):
                categories.append(SafetyCategoryResult.from_dict(item))
            elif item is not None:
                categories.append(SafetyCategoryResult(category=_coerce_str(item)))
        category_scores = _normalize_category_scores(data.get("category_scores") or data.get("scores"))
        return cls(
            flagged=_coerce_bool(data.get("flagged")),
            categories=categories,
            category_scores=category_scores,
            rationale=_coerce_str(data.get("rationale")) or None,
            raw=dict(data),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "flagged": self.flagged,
            "categories": [category.to_dict() for category in self.categories],
            "category_scores": dict(self.category_scores),
            "raw": dict(self.raw),
        }
        if self.rationale is not None:
            payload["rationale"] = self.rationale
        return payload


def normalize_text_for_safety(text: Any) -> str:
    value = _coerce_str(text)
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    return value.strip()


def normalize_category_thresholds(thresholds: Any) -> Dict[str, float]:
    if thresholds is None:
        return {}
    if isinstance(thresholds, Mapping):
        return {str(k): _coerce_float(v) for k, v in thresholds.items()}
    normalized: Dict[str, float] = {}
    for item in _coerce_list(thresholds):
        if isinstance(item, Mapping):
            name = item.get("category") or item.get("name") or item.get("key")
            if name is not None:
                normalized[str(name)] = _coerce_float(item.get("threshold", item.get("score", 0.0)))
    return normalized


def merge_category_scores(*sources: Any) -> Dict[str, float]:
    merged: Dict[str, float] = {}
    for source in sources:
        merged.update(_normalize_category_scores(source))
    return merged


def response_flagged_categories(response: Union[SafetyResponse, Mapping[str, Any]]) -> List[str]:
    if isinstance(response, SafetyResponse):
        return [item.category for item in response.categories if item.flagged and item.category]
    normalized = SafetyResponse.from_dict(response)
    return [item.category for item in normalized.categories if item.flagged and item.category]


def response_max_score(response: Union[SafetyResponse, Mapping[str, Any]]) -> float:
    if isinstance(response, SafetyResponse):
        scores = list(response.category_scores.values()) or [item.score for item in response.categories]
    else:
        normalized = SafetyResponse.from_dict(response)
        scores = list(normalized.category_scores.values()) or [item.score for item in normalized.categories]
    return max(scores) if scores else 0.0
