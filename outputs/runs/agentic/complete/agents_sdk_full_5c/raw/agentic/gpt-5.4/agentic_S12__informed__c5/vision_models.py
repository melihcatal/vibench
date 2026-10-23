from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ImageLabel:
    name: str
    confidence: float


@dataclass
class OCRLine:
    text: str
    confidence: float


@dataclass
class SafetyCategory:
    name: str
    confidence: float


@dataclass
class DetectionResult:
    provider: str
    image_uri: Optional[str] = None
    labels: List[ImageLabel] = field(default_factory=list)
    description: Optional[str] = None
    ocr_lines: List[OCRLine] = field(default_factory=list)
    safety_categories: List[SafetyCategory] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "image_uri": self.image_uri,
            "labels": [label.__dict__ for label in self.labels],
            "description": self.description,
            "ocr_lines": [line.__dict__ for line in self.ocr_lines],
            "safety_categories": [cat.__dict__ for cat in self.safety_categories],
            "raw": self.raw,
        }


def top_labels(labels: Iterable[ImageLabel], limit: int = 5) -> List[ImageLabel]:
    return sorted(labels, key=lambda item: item.confidence, reverse=True)[:limit]


def join_ocr_text(lines: Iterable[OCRLine]) -> str:
    return "\n".join(line.text for line in lines if line.text.strip())


def summarize_safety(categories: Iterable[SafetyCategory], threshold: float = 0.5) -> Dict[str, Any]:
    items = sorted(categories, key=lambda item: item.confidence, reverse=True)
    flagged = [item.name for item in items if item.confidence >= threshold]
    return {
        "flagged": bool(flagged),
        "categories": [item.__dict__ for item in items],
        "flagged_categories": flagged,
    }
