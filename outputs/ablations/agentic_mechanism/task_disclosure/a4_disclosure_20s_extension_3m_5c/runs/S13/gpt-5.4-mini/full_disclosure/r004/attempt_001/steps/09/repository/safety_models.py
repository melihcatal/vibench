import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def _coerce_text_input(text: Any) -> Any:
    if isinstance(text, str):
        return text
    if isinstance(text, list) and all(isinstance(item, str) for item in text):
        return text
    raise TypeError("input must be a string or list of strings")


def _coerce_thresholds(thresholds: Optional[Mapping[str, Any]]) -> Dict[str, float]:
    if thresholds is None:
        return {
            "harassment": 0.5,
            "hate": 0.5,
            "self-harm": 0.5,
            "sexual": 0.5,
            "violence": 0.5,
        }
    if not isinstance(thresholds, Mapping):
        raise TypeError("thresholds must be a mapping")
    normalized: Dict[str, float] = {}
    for category, value in thresholds.items():
        if not isinstance(category, str):
            raise TypeError("threshold keys must be strings")
        if not isinstance(value, (int, float)):
            raise TypeError("threshold values must be numeric")
        normalized[category] = float(value)
    return normalized


def _coerce_scores(scores: Optional[Mapping[str, Any]]) -> Dict[str, float]:
    if scores is None:
        return {}
    if not isinstance(scores, Mapping):
        raise TypeError("scores must be a mapping")
    normalized: Dict[str, float] = {}
    for category, value in scores.items():
        if not isinstance(category, str):
            raise TypeError("score keys must be strings")
        if not isinstance(value, (int, float)):
            raise TypeError("score values must be numeric")
        normalized[category] = float(value)
    return normalized


def _coerce_categories(categories: Optional[Mapping[str, Any]]) -> Dict[str, bool]:
    if categories is None:
        return {}
    if not isinstance(categories, Mapping):
        raise TypeError("categories must be a mapping")
    normalized: Dict[str, bool] = {}
    for category, value in categories.items():
        if not isinstance(category, str):
            raise TypeError("category keys must be strings")
        normalized[category] = bool(value)
    return normalized


def _coerce_spans(spans: Optional[Iterable[Mapping[str, Any]]]) -> List[Dict[str, Any]]:
    if spans is None:
        return []
    if not isinstance(spans, Iterable):
        raise TypeError("spans must be iterable")
    normalized: List[Dict[str, Any]] = []
    for span in spans:
        if not isinstance(span, Mapping):
            raise TypeError("each span must be a mapping")
        normalized.append(dict(span))
    return normalized


@dataclass(frozen=True)
class SafetyRequest:
    input: Any
    model: str = OPENAI_MODERATION_MODEL

    def __post_init__(self) -> None:
        object.__setattr__(self, "input", _coerce_text_input(self.input))
        if not isinstance(self.model, str) or not self.model:
            raise TypeError("model must be a non-empty string")

    def to_payload(self) -> Dict[str, Any]:
        return {"model": self.model, "input": self.input}


@dataclass(frozen=True)
class SafetyThresholds:
    categories: Dict[str, float] = field(default_factory=_coerce_thresholds)

    def __post_init__(self) -> None:
        object.__setattr__(self, "categories", _coerce_thresholds(self.categories))


@dataclass(frozen=True)
class SafetyResult:
    provider: str
    model: str
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    raw: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        if not isinstance(self.provider, str) or not self.provider:
            raise TypeError("provider must be a non-empty string")
        if not isinstance(self.model, str) or not self.model:
            raise TypeError("model must be a non-empty string")
        object.__setattr__(self, "flagged", bool(self.flagged))
        object.__setattr__(self, "categories", _coerce_categories(self.categories))
        object.__setattr__(self, "category_scores", _coerce_scores(self.category_scores))
        if self.raw is not None and not isinstance(self.raw, dict):
            raise TypeError("raw must be a dictionary or None")

    @classmethod
    def from_api_response(cls, response: Mapping[str, Any], model: Optional[str] = None) -> "SafetyResult":
        if not isinstance(response, Mapping):
            raise TypeError("response must be a mapping")
        results = response.get("results") or []
        first = results[0] if results else {}
        resolved_model = model or str(response.get("model") or OPENAI_MODERATION_MODEL)
        return cls(
            provider="openai",
            model=resolved_model,
            flagged=bool(first.get("flagged", False)),
            categories=_coerce_categories(first.get("categories") or {}),
            category_scores=_coerce_scores(first.get("category_scores") or {}),
            raw=dict(response),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "flagged": self.flagged,
            "categories": dict(self.categories),
            "category_scores": dict(self.category_scores),
            "raw": self.raw,
        }


@dataclass(frozen=True)
class ThresholdCheck:
    score: float
    threshold: float
    triggered: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "score", float(self.score))
        object.__setattr__(self, "threshold", float(self.threshold))
        object.__setattr__(self, "triggered", bool(self.triggered))


@dataclass(frozen=True)
class SafetyDecision:
    allow: bool
    thresholds: Dict[str, float]
    threshold_checks: Dict[str, ThresholdCheck]
    result: SafetyResult

    def __post_init__(self) -> None:
        object.__setattr__(self, "allow", bool(self.allow))
        object.__setattr__(self, "thresholds", _coerce_thresholds(self.thresholds))
        if not isinstance(self.threshold_checks, Mapping):
            raise TypeError("threshold_checks must be a mapping")
        checks: Dict[str, ThresholdCheck] = {}
        for category, check in self.threshold_checks.items():
            if not isinstance(category, str):
                raise TypeError("threshold check keys must be strings")
            if isinstance(check, ThresholdCheck):
                checks[category] = check
            elif isinstance(check, Mapping):
                checks[category] = ThresholdCheck(
                    score=check.get("score", 0.0),
                    threshold=check.get("threshold", 0.0),
                    triggered=check.get("triggered", False),
                )
            else:
                raise TypeError("threshold checks must contain ThresholdCheck or mapping values")
        object.__setattr__(self, "threshold_checks", checks)
        if not isinstance(self.result, SafetyResult):
            raise TypeError("result must be a SafetyResult")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "allow": self.allow,
            "thresholds": dict(self.thresholds),
            "threshold_checks": {
                category: {
                    "score": check.score,
                    "threshold": check.threshold,
                    "triggered": check.triggered,
                }
                for category, check in self.threshold_checks.items()
            },
            "result": self.result.to_dict(),
        }
