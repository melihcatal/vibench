from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class ImageAnalysisRequest:
    image_path: str
    image_url: Optional[str] = None
    language: Optional[str] = None
    max_results: int = 10
    threshold: float = 0.0


@dataclass
class VisionLabel:
    name: str
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionTextBlock:
    text: str
    confidence: float = 0.0
    bbox: Optional[Dict[str, Any]] = None


@dataclass
class VisionSafetyScore:
    label: str
    score: float = 0.0
    flagged: bool = False
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionResponse:
    provider: str
    raw: Any
    labels: List[VisionLabel] = field(default_factory=list)
    text_blocks: List[VisionTextBlock] = field(default_factory=list)
    safety: List[VisionSafetyScore] = field(default_factory=list)
    summary: Optional[str] = None


def _as_mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if hasattr(value, "__dict__"):
        return value.__dict__
    return {}


def normalize_labels(items: Iterable[Any]) -> List[VisionLabel]:
    normalized: List[VisionLabel] = []
    for item in items:
        data = _as_mapping(item)
        name = str(data.get("name") or data.get("description") or data.get("label") or "")
        confidence = float(data.get("confidence") or data.get("score") or 0.0)
        normalized.append(VisionLabel(name=name, confidence=confidence, metadata=dict(data)))
    return normalized


def normalize_text(items: Iterable[Any]) -> List[VisionTextBlock]:
    normalized: List[VisionTextBlock] = []
    for item in items:
        data = _as_mapping(item)
        text = str(data.get("text") or data.get("description") or data.get("content") or "")
        confidence = float(data.get("confidence") or data.get("score") or 0.0)
        bbox = data.get("bounding_box") or data.get("bbox")
        normalized.append(VisionTextBlock(text=text, confidence=confidence, bbox=bbox))
    return normalized


def normalize_safety(items: Iterable[Any]) -> List[VisionSafetyScore]:
    normalized: List[VisionSafetyScore] = []
    for item in items:
        data = _as_mapping(item)
        label = str(data.get("label") or data.get("category") or data.get("name") or "")
        score = float(data.get("score") or data.get("confidence") or 0.0)
        flagged = bool(data.get("flagged") or data.get("unsafe") or score >= 0.5)
        normalized.append(VisionSafetyScore(label=label, score=score, flagged=flagged, details=dict(data)))
    return normalized
