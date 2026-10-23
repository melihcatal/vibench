from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageSource:
    image_path: str
    mime_type: Optional[str] = None


@dataclass
class LabelDetectionResult:
    name: str
    confidence: float
    parents: List[str] = field(default_factory=list)


@dataclass
class ImageDescriptionResult:
    text: str
    confidence: Optional[float] = None


@dataclass
class OCRTextBlock:
    text: str
    confidence: Optional[float] = None
    block_type: Optional[str] = None


@dataclass
class SafetyCategoryScore:
    category: str
    score: float


@dataclass
class SafetyResult:
    is_safe: bool
    categories: List[SafetyCategoryScore]
    reasons: List[str] = field(default_factory=list)


@dataclass
class ArchiveArtifact:
    key: str
    bucket: str
    etag: Optional[str] = None
    url: Optional[str] = None


@dataclass
class SummaryResult:
    summary: str
    model: str


@dataclass
class TranslationResult:
    translated_text: str
    target_language: str
    provider: str


@dataclass
class TextSafetyResult:
    flagged: bool
    scores: Dict[str, float]
    provider: str


def dataclass_to_dict(instance: Any) -> Dict[str, Any]:
    return asdict(instance)


def normalize_labels(items: List[Dict[str, Any]]) -> List[LabelDetectionResult]:
    return [
        LabelDetectionResult(
            name=str(item.get("name", "")),
            confidence=float(item.get("confidence", 0.0)),
            parents=list(item.get("parents", [])),
        )
        for item in items
    ]


def normalize_text_blocks(items: List[Dict[str, Any]]) -> List[OCRTextBlock]:
    return [
        OCRTextBlock(
            text=str(item.get("text", "")),
            confidence=item.get("confidence"),
            block_type=item.get("block_type"),
        )
        for item in items
    ]
