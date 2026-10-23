from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class VisionImageRequest:
    image_path: str
    language: Optional[str] = None
    max_results: int = 10
    detail: str = "short"


@dataclass
class VisionLabel:
    name: str
    confidence: float
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionTextBlock:
    text: str
    confidence: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionSafetyResult:
    unsafe: bool
    score: float
    categories: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionDescription:
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ArchivePayload:
    object_key: str
    metadata: Dict[str, Any]
    body: bytes


def normalize_labels(labels: List[Dict[str, Any]]) -> List[VisionLabel]:
    return [
        VisionLabel(
            name=str(item.get("name", "")),
            confidence=float(item.get("confidence", 0.0)),
            raw=item,
        )
        for item in labels
    ]


def normalize_text_blocks(blocks: List[Dict[str, Any]]) -> List[VisionTextBlock]:
    return [
        VisionTextBlock(
            text=str(item.get("text", "")),
            confidence=(float(item["confidence"]) if item.get("confidence") is not None else None),
            raw=item,
        )
        for item in blocks
    ]


def compact_description(labels: List[VisionLabel], text_blocks: List[VisionTextBlock]) -> str:
    parts = [label.name for label in labels[:3] if label.name]
    if text_blocks:
        parts.append(f'text: {text_blocks[0].text[:80]}')
    return ", ".join(parts) if parts else "image content"
