from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class VisionRequest:
    image_path: str
    language_hint: Optional[str] = None


@dataclass
class VisionLabel:
    name: str
    score: float = 0.0


@dataclass
class VisionTextBlock:
    text: str
    confidence: float = 0.0


@dataclass
class VisionSafetyResult:
    unsafe: bool
    categories: Dict[str, float] = field(default_factory=dict)


def normalize_labels(items: List[Any]) -> List[VisionLabel]:
    normalized = []
    for item in items:
        normalized.append(
            VisionLabel(
                name=getattr(item, "description", str(item)),
                score=float(getattr(item, "score", 0.0)),
            )
        )
    return normalized


def normalize_text(items: List[Any]) -> List[VisionTextBlock]:
    normalized = []
    for item in items:
        normalized.append(
            VisionTextBlock(
                text=getattr(item, "description", str(item)),
                confidence=float(getattr(item, "score", 0.0)),
            )
        )
    return normalized
