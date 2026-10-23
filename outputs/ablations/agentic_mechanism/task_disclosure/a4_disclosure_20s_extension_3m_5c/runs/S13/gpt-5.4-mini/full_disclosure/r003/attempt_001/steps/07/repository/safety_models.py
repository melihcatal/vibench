from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Sequence


DEFAULT_SAFETY_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def _to_dict(value: Any) -> Dict[str, Any]:
    if hasattr(value, "model_dump"):
        return dict(value.model_dump())
    if isinstance(value, dict):
        return dict(value)
    return dict(value)


def _coerce_thresholds(thresholds: Optional[Mapping[str, float]]) -> Dict[str, float]:
    if not thresholds:
        return {}
    return {str(key): float(value) for key, value in thresholds.items()}


@dataclass(frozen=True)
class SafetyRequest:
    text: str
    model: str = DEFAULT_SAFETY_MODEL
    thresholds: Dict[str, float] = field(default_factory=dict)

    @classmethod
    def normalize(cls, value: Any, *, default_model: Optional[str] = None) -> "SafetyRequest":
        if isinstance(value, cls):
            return cls(text=value.text, model=value.model or (default_model or DEFAULT_SAFETY_MODEL), thresholds=dict(value.thresholds))
        if isinstance(value, str):
            return cls(text=value, model=default_model or DEFAULT_SAFETY_MODEL, thresholds={})
        if isinstance(value, Mapping):
            text = str(value.get("text", ""))
            model = str(value.get("model") or default_model or DEFAULT_SAFETY_MODEL)
            thresholds = _coerce_thresholds(value.get("thresholds"))
            return cls(text=text, model=model, thresholds=thresholds)
        raise TypeError("Unsupported safety request type")


@dataclass(frozen=True)
class SafetyResult:
    model: str
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    allow: Optional[bool] = None
    triggered_thresholds: Dict[str, Dict[str, float]] = field(default_factory=dict)
    thresholds: Dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_moderation(cls, result: Any, *, model: Optional[str] = None) -> "SafetyResult":
        categories = _to_dict(result.categories)
        category_scores = _to_dict(result.category_scores)
        return cls(
            model=model or getattr(result, "model", DEFAULT_SAFETY_MODEL),
            flagged=bool(result.flagged),
            categories={str(key): bool(value) for key, value in categories.items()},
            category_scores={str(key): float(value) for key, value in category_scores.items()},
        )

    def with_decision(self, *, allow: bool, triggered_thresholds: Mapping[str, Mapping[str, float]], thresholds: Mapping[str, float]) -> "SafetyResult":
        return SafetyResult(
            model=self.model,
            flagged=self.flagged,
            categories=dict(self.categories),
            category_scores=dict(self.category_scores),
            allow=bool(allow),
            triggered_thresholds={str(key): {str(k): float(v) for k, v in value.items()} for key, value in triggered_thresholds.items()},
            thresholds={str(key): float(value) for key, value in thresholds.items()},
        )


def normalize_text_input(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        return str(value.get("text", ""))
    raise TypeError("Unsupported text input type")


def normalize_messages(value: Any) -> Sequence[str]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [str(item) for item in value]
    raise TypeError("Unsupported messages type")


def normalize_moderation_result(value: Any, *, model: Optional[str] = None) -> Dict[str, Any]:
    result = SafetyResult.from_moderation(value, model=model)
    output: Dict[str, Any] = {
        "model": result.model,
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
    if result.allow is not None:
        output["allow"] = bool(result.allow)
    if result.triggered_thresholds:
        output["triggered_thresholds"] = dict(result.triggered_thresholds)
    if result.thresholds:
        output["thresholds"] = dict(result.thresholds)
    return output
