from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


TextInput = Union[str, Sequence[str]]


def _coerce_texts(value: TextInput) -> List[str]:
    if isinstance(value, str):
        texts = [value]
    else:
        texts = list(value)
    normalized: List[str] = []
    for item in texts:
        if not isinstance(item, str):
            raise TypeError("text values must be strings")
        normalized.append(item)
    return normalized


def _clamp_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = 0.0
    return max(0.0, min(1.0, score))


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


@dataclass(frozen=True)
class TextSafetyRequest:
    text: TextInput
    categories: Optional[Sequence[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalize(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": _coerce_texts(self.text)}
        if self.categories is not None:
            payload["categories"] = [str(category) for category in self.categories]
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class SafetyCategoryResult:
    category: str
    score: float = 0.0
    flagged: bool = False

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SafetyCategoryResult":
        return cls(
            category=str(value.get("category", "")),
            score=_clamp_score(value.get("score", 0.0)),
            flagged=_coerce_bool(value.get("flagged", False)),
        )

    def normalize(self) -> Dict[str, Any]:
        return {"category": self.category, "score": _clamp_score(self.score), "flagged": bool(self.flagged)}


@dataclass(frozen=True)
class TextSafetyResponse:
    text: str
    flagged: bool = False
    categories: List[SafetyCategoryResult] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TextSafetyResponse":
        categories = value.get("categories", [])
        parsed_categories: List[SafetyCategoryResult] = []
        if isinstance(categories, Sequence) and not isinstance(categories, (str, bytes, bytearray)):
            for item in categories:
                if isinstance(item, Mapping):
                    parsed_categories.append(SafetyCategoryResult.from_mapping(item))
        return cls(
            text=str(value.get("text", "")),
            flagged=_coerce_bool(value.get("flagged", False)),
            categories=parsed_categories,
            raw=dict(value),
        )

    def normalize(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "flagged": bool(self.flagged),
            "categories": [category.normalize() for category in self.categories],
        }


def normalize_text_safety_request(request: Union[TextSafetyRequest, Mapping[str, Any], TextInput]) -> Dict[str, Any]:
    if isinstance(request, TextSafetyRequest):
        return request.normalize()
    if isinstance(request, Mapping):
        return TextSafetyRequest(
            text=request.get("text", ""),
            categories=request.get("categories"),
            metadata=dict(request.get("metadata", {})) if isinstance(request.get("metadata", {}), Mapping) else {},
        ).normalize()
    return TextSafetyRequest(text=request).normalize()


def normalize_text_safety_response(response: Union[TextSafetyResponse, Mapping[str, Any]]) -> Dict[str, Any]:
    if isinstance(response, TextSafetyResponse):
        return response.normalize()
    return TextSafetyResponse.from_mapping(response).normalize()


def parse_text_safety_response(response: Mapping[str, Any]) -> TextSafetyResponse:
    return TextSafetyResponse.from_mapping(response)
