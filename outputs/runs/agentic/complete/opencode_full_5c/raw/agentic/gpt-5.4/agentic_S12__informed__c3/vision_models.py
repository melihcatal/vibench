from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class ImageSource:
    image_path: Optional[str] = None
    image_uri: Optional[str] = None


@dataclass
class LabelDetectionResult:
    provider: str
    labels: List[Dict[str, Any]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ImageDescriptionResult:
    provider: str
    description: str
    model: str
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TextDetectionResult:
    provider: str
    text: str
    annotations: List[Dict[str, Any]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ImageSafetyResult:
    provider: str
    categories: List[Dict[str, Any]] = field(default_factory=list)
    blocked: bool = False
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ImageSummaryResult:
    provider: str
    model: str
    summary: str
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TranslationResult:
    provider: str
    target_language: str
    translated_text: str
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TextSafetyResult:
    provider: str
    flagged: bool
    scores: Dict[str, float] = field(default_factory=dict)
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ArchiveResult:
    provider: str
    bucket: str
    object_name: str
    uri: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_label_annotations(items: List[Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items:
        normalized.append(
            {
                "name": getattr(item, "description", None)
                or getattr(item, "name", None),
                "score": float(getattr(item, "score", 0.0) or 0.0),
            }
        )
    return normalized


def normalize_text_annotations(items: List[Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items:
        normalized.append(
            {
                "text": getattr(item, "description", None),
                "locale": getattr(item, "locale", None),
            }
        )
    return normalized


def serialize_dataclass(result: Any) -> Dict[str, Any]:
    if hasattr(result, "to_dict"):
        return result.to_dict()
    if hasattr(result, "__dataclass_fields__"):
        return asdict(result)
    raise TypeError("Unsupported result type")
