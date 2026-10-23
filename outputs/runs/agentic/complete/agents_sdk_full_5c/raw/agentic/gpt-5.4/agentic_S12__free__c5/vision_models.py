from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageLabel:
    name: str
    confidence: float


@dataclass
class OCRTextBlock:
    text: str
    confidence: float
    block_type: str = "LINE"


@dataclass
class SafetyCategory:
    name: str
    confidence: float


@dataclass
class VisualDescription:
    text: str
    model: str
    provider: str


@dataclass
class ImageAnalysisResult:
    image_uri: str
    labels: List[ImageLabel] = field(default_factory=list)
    text_blocks: List[OCRTextBlock] = field(default_factory=list)
    safety_categories: List[SafetyCategory] = field(default_factory=list)
    description: Optional[VisualDescription] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image_uri": self.image_uri,
            "labels": [vars(item) for item in self.labels],
            "text_blocks": [vars(item) for item in self.text_blocks],
            "safety_categories": [vars(item) for item in self.safety_categories],
            "description": vars(self.description) if self.description else None,
        }


def normalize_confidence(value: Optional[float], scale: float = 1.0) -> float:
    if value is None:
        return 0.0
    return round(float(value) * scale, 4)


def top_label_names(labels: List[ImageLabel], limit: int = 10) -> List[str]:
    return [label.name for label in sorted(labels, key=lambda x: x.confidence, reverse=True)[:limit]]


def merge_text_blocks(blocks: List[OCRTextBlock]) -> str:
    return "\n".join(block.text for block in blocks if block.text.strip())


def compact_safety_map(categories: List[SafetyCategory]) -> Dict[str, float]:
    return {item.name: item.confidence for item in categories}
