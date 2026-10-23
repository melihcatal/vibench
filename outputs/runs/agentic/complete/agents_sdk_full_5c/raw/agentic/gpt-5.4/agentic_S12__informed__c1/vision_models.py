from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageSource:
    image_path: str


@dataclass
class LabelDetectionResult:
    provider: str
    labels: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ImageDescriptionResult:
    provider: str
    description: str
    model: Optional[str] = None


@dataclass
class OCRResult:
    provider: str
    text: str
    blocks: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ImageSafetyResult:
    provider: str
    safe_search: Dict[str, Any] = field(default_factory=dict)
    flagged: bool = False


@dataclass
class SummaryResult:
    provider: str
    summary: str
    model: Optional[str] = None


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None


@dataclass
class TextSafetyResult:
    provider: str
    scores: Dict[str, Any] = field(default_factory=dict)
    flagged: bool = False


@dataclass
class ArchiveResult:
    provider: str
    bucket: str
    key: str
    uri: str


LIKELIHOOD_ORDER = {
    "UNKNOWN": 0,
    "VERY_UNLIKELY": 1,
    "UNLIKELY": 2,
    "POSSIBLE": 3,
    "LIKELY": 4,
    "VERY_LIKELY": 5,
}


def normalize_label_annotations(label_annotations: List[Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in label_annotations or []:
        normalized.append(
            {
                "description": getattr(item, "description", None),
                "score": float(getattr(item, "score", 0.0) or 0.0),
                "topicality": float(getattr(item, "topicality", 0.0) or 0.0),
            }
        )
    return normalized


def normalize_text_annotations(text_annotations: List[Any]) -> Dict[str, Any]:
    if not text_annotations:
        return {"text": "", "blocks": []}
    full_text = getattr(text_annotations[0], "description", "") or ""
    blocks: List[Dict[str, Any]] = []
    for item in text_annotations[1:]:
        blocks.append(
            {
                "text": getattr(item, "description", None),
                "confidence": getattr(item, "confidence", None),
            }
        )
    return {"text": full_text, "blocks": blocks}


def normalize_safe_search(safe_search_annotation: Any) -> Dict[str, Any]:
    if safe_search_annotation is None:
        return {}
    return {
        "adult": getattr(safe_search_annotation, "adult", None),
        "spoof": getattr(safe_search_annotation, "spoof", None),
        "medical": getattr(safe_search_annotation, "medical", None),
        "violence": getattr(safe_search_annotation, "violence", None),
        "racy": getattr(safe_search_annotation, "racy", None),
    }


def is_safe_search_flagged(safe_search: Dict[str, Any]) -> bool:
    for key in ("adult", "violence", "racy"):
        value = safe_search.get(key)
        if value is None:
            continue
        if LIKELIHOOD_ORDER.get(str(value), 0) >= LIKELIHOOD_ORDER["LIKELY"]:
            return True
    return False
