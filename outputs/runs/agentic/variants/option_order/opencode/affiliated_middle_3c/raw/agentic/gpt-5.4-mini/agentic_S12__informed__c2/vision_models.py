from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VisionRequest:
    image_path: str
    prompt: Optional[str] = None
    language: Optional[str] = None


@dataclass
class VisionLabel:
    name: str
    score: float


@dataclass
class VisionTextBlock:
    text: str
    confidence: float


@dataclass
class VisionSafetyResult:
    unsafe: bool
    categories: Dict[str, float]


def normalize_labels(items: List[Dict[str, Any]]) -> List[VisionLabel]:
    return [
        VisionLabel(name=str(item.get("name", "")), score=float(item.get("score", 0.0)))
        for item in items
    ]


def normalize_text_blocks(items: List[Dict[str, Any]]) -> List[VisionTextBlock]:
    return [
        VisionTextBlock(
            text=str(item.get("text", "")),
            confidence=float(item.get("confidence", 0.0)),
        )
        for item in items
    ]
