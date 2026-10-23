from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class ImageSource:
    path: Optional[str] = None
    uri: Optional[str] = None
    mime_type: Optional[str] = None


@dataclass
class LabelDetection:
    name: str
    confidence: float
    categories: List[str] = field(default_factory=list)


@dataclass
class OCRLine:
    text: str
    confidence: float
    bounding_box: Optional[List[Dict[str, Any]]] = None


@dataclass
class SafetyAttribute:
    name: str
    confidence: float


@dataclass
class VisionResult:
    provider: str
    model: str
    image: Dict[str, Any]
    labels: List[LabelDetection] = field(default_factory=list)
    description: Optional[str] = None
    extracted_text: List[OCRLine] = field(default_factory=list)
    safety: List[SafetyAttribute] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_confidence(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0
    if numeric > 1.0:
        return round(numeric / 100.0, 4)
    return round(numeric, 4)


def compact_text(lines: List[OCRLine]) -> str:
    return "\n".join(line.text for line in lines if line.text.strip())


def labels_to_strings(labels: List[LabelDetection], min_confidence: float = 0.0) -> List[str]:
    return [label.name for label in labels if label.confidence >= min_confidence]
