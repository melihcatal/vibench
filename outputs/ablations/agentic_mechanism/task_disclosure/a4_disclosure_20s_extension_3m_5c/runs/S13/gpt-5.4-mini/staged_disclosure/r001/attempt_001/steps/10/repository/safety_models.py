from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Mapping, MutableMapping, Optional


class SafetyLabel(str, Enum):
    SAFE = "safe"
    UNSAFE = "unsafe"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class TextSafetyRequest:
    text: str
    language: Optional[str] = None
    categories: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"text": self.text}
        if self.language is not None:
            data["language"] = self.language
        if self.categories:
            data["categories"] = list(self.categories)
        return data


@dataclass(frozen=True)
class SafetyCategoryScore:
    category: str
    score: float
    flagged: bool = False

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "SafetyCategoryScore":
        return cls(
            category=str(data.get("category", "")),
            score=float(data.get("score", 0.0)),
            flagged=bool(data.get("flagged", False)),
        )


@dataclass(frozen=True)
class TextSafetyResponse:
    label: SafetyLabel
    confidence: float
    categories: tuple[SafetyCategoryScore, ...] = field(default_factory=tuple)
    raw: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_safe(self) -> bool:
        return self.label == SafetyLabel.SAFE


def _coerce_label(value: Any) -> SafetyLabel:
    if isinstance(value, SafetyLabel):
        return value
    if value is None:
        return SafetyLabel.UNKNOWN
    normalized = str(value).strip().lower()
    if normalized in {SafetyLabel.SAFE.value, "clean", "ok"}:
        return SafetyLabel.SAFE
    if normalized in {SafetyLabel.UNSAFE.value, "unsafe_content", "flagged"}:
        return SafetyLabel.UNSAFE
    return SafetyLabel.UNKNOWN


def normalize_text_safety_response(payload: Mapping[str, Any]) -> TextSafetyResponse:
    label_value = payload.get("label", payload.get("safety_label", payload.get("verdict")))
    confidence_value = payload.get("confidence", payload.get("score", 0.0))

    categories_payload = payload.get("categories", payload.get("category_scores", []))
    categories: list[SafetyCategoryScore] = []
    if isinstance(categories_payload, list):
        for item in categories_payload:
            if isinstance(item, Mapping):
                categories.append(SafetyCategoryScore.from_mapping(item))

    raw: Dict[str, Any] = dict(payload)
    return TextSafetyResponse(
        label=_coerce_label(label_value),
        confidence=float(confidence_value or 0.0),
        categories=tuple(categories),
        raw=raw,
    )


def normalize_text_safety_request(data: Mapping[str, Any]) -> TextSafetyRequest:
    text = str(data.get("text", ""))
    language = data.get("language")
    categories_value = data.get("categories", ())
    categories: tuple[str, ...]
    if isinstance(categories_value, (list, tuple)):
        categories = tuple(str(item) for item in categories_value)
    else:
        categories = ()
    return TextSafetyRequest(text=text, language=None if language is None else str(language), categories=categories)


def response_to_mapping(response: TextSafetyResponse) -> Dict[str, Any]:
    return {
        "label": response.label.value,
        "confidence": response.confidence,
        "categories": [
            {"category": item.category, "score": item.score, "flagged": item.flagged}
            for item in response.categories
        ],
    }
