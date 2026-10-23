from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class ImageSource:
    path: Optional[str] = None
    uri: Optional[str] = None
    content_bytes: Optional[bytes] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "uri": self.uri,
            "has_content_bytes": self.content_bytes is not None,
        }


@dataclass
class LabelDetection:
    name: str
    confidence: float
    categories: List[str] = field(default_factory=list)


@dataclass
class TextBlock:
    text: str
    confidence: float
    language: Optional[str] = None


@dataclass
class SafetyCategoryScore:
    category: str
    confidence: float


@dataclass
class VisionResult:
    provider: str
    model: Optional[str] = None
    labels: List[LabelDetection] = field(default_factory=list)
    description: Optional[str] = None
    text_blocks: List[TextBlock] = field(default_factory=list)
    safety_scores: List[SafetyCategoryScore] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.raw_response is None:
            data["raw_response"] = None
        return data


def normalize_confidence(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0
    if numeric > 1.0:
        return round(numeric / 100.0, 6)
    return round(numeric, 6)


def top_label_names(result: VisionResult, limit: int = 10) -> List[str]:
    ordered = sorted(result.labels, key=lambda item: item.confidence, reverse=True)
    return [item.name for item in ordered[:limit]]


def join_detected_text(result: VisionResult) -> str:
    parts = [block.text.strip() for block in result.text_blocks if block.text and block.text.strip()]
    return "\n".join(parts)


def safety_map(result: VisionResult) -> Dict[str, float]:
    return {item.category: item.confidence for item in result.safety_scores}
