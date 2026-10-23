from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class ImageSource:
    image_bytes: Optional[bytes] = None
    image_uri: Optional[str] = None
    mime_type: str = "image/jpeg"

    def is_remote(self) -> bool:
        return bool(self.image_uri)


@dataclass(slots=True)
class DetectionLabel:
    name: str
    score: float
    category: Optional[str] = None


@dataclass(slots=True)
class OCRTextBlock:
    text: str
    score: float
    block_type: str = "LINE"


@dataclass(slots=True)
class SafetyAttribute:
    name: str
    confidence: float


@dataclass(slots=True)
class VisualDescription:
    text: str
    model: str
    provider: str


@dataclass(slots=True)
class AnalysisSummary:
    labels: List[str] = field(default_factory=list)
    description: Optional[str] = None
    extracted_text: List[str] = field(default_factory=list)
    safety_flags: List[str] = field(default_factory=list)


def normalize_google_labels(response: Any) -> List[DetectionLabel]:
    labels: List[DetectionLabel] = []
    for item in getattr(response, "label_annotations", []) or []:
        labels.append(
            DetectionLabel(
                name=getattr(item, "description", ""),
                score=float(getattr(item, "score", 0.0)),
                category="label",
            )
        )
    for item in getattr(response, "localized_object_annotations", []) or []:
        labels.append(
            DetectionLabel(
                name=getattr(item, "name", ""),
                score=float(getattr(item, "score", 0.0)),
                category="object",
            )
        )
    return labels


def normalize_google_ocr(response: Any) -> List[OCRTextBlock]:
    annotations = getattr(response, "text_annotations", []) or []
    blocks: List[OCRTextBlock] = []
    for index, item in enumerate(annotations):
        if index == 0:
            continue
        blocks.append(
            OCRTextBlock(
                text=getattr(item, "description", ""),
                score=1.0,
                block_type="WORD",
            )
        )
    if not blocks and annotations:
        blocks.append(OCRTextBlock(text=getattr(annotations[0], "description", ""), score=1.0, block_type="FULL_TEXT"))
    return blocks


def normalize_google_safe_search(response: Any) -> List[SafetyAttribute]:
    safe = getattr(response, "safe_search_annotation", None)
    if safe is None:
        return []
    names = ["adult", "spoof", "medical", "violence", "racy"]
    attrs: List[SafetyAttribute] = []
    for name in names:
        value = getattr(safe, name, 0)
        attrs.append(SafetyAttribute(name=name, confidence=float(value)))
    return attrs


def coerce_summary(payload: Dict[str, Any]) -> AnalysisSummary:
    return AnalysisSummary(
        labels=list(payload.get("labels", []) or []),
        description=payload.get("description"),
        extracted_text=list(payload.get("extracted_text", []) or []),
        safety_flags=list(payload.get("safety_flags", []) or []),
    )
