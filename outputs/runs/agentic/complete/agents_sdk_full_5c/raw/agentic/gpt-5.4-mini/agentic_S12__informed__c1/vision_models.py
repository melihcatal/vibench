from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


@dataclass
class VisionRequest:
    image_path: str
    max_results: int = 10
    language: Optional[str] = None
    threshold: Optional[float] = None


@dataclass
class LabelResult:
    name: str
    score: float


@dataclass
class TextResult:
    text: str
    confidence: Optional[float] = None


@dataclass
class SafetyResult:
    unsafe: bool
    categories: List[str] = field(default_factory=list)
    score: Optional[float] = None


@dataclass
class ImageDescription:
    caption: str
    confidence: Optional[float] = None


@dataclass
class VisionResponse:
    raw: Any
    labels: List[LabelResult] = field(default_factory=list)
    texts: List[TextResult] = field(default_factory=list)
    safety: Optional[SafetyResult] = None
    description: Optional[ImageDescription] = None


def normalize_labels(items: Any) -> List[LabelResult]:
    results: List[LabelResult] = []
    for item in items or []:
        if isinstance(item, Mapping):
            name = str(item.get("name") or item.get("description") or item.get("label") or "")
            score = float(item.get("score") or item.get("confidence") or 0.0)
        else:
            name = str(getattr(item, "name", getattr(item, "description", "")))
            score = float(getattr(item, "score", getattr(item, "confidence", 0.0)))
        if name:
            results.append(LabelResult(name=name, score=score))
    return results


def normalize_texts(items: Any) -> List[TextResult]:
    results: List[TextResult] = []
    for item in items or []:
        if isinstance(item, Mapping):
            text = str(item.get("text") or item.get("description") or item.get("value") or "")
            confidence = item.get("confidence") or item.get("score")
        else:
            text = str(getattr(item, "text", getattr(item, "description", "")))
            confidence = getattr(item, "confidence", getattr(item, "score", None))
        if text:
            results.append(TextResult(text=text, confidence=None if confidence is None else float(confidence)))
    return results


def normalize_description(value: Any) -> ImageDescription:
    if isinstance(value, Mapping):
        caption = str(value.get("caption") or value.get("description") or value.get("text") or "")
        confidence = value.get("confidence") or value.get("score")
    else:
        caption = str(getattr(value, "caption", getattr(value, "description", getattr(value, "text", ""))))
        confidence = getattr(value, "confidence", getattr(value, "score", None))
    return ImageDescription(caption=caption, confidence=None if confidence is None else float(confidence))


def normalize_safety(value: Any) -> SafetyResult:
    if isinstance(value, Mapping):
        unsafe = bool(value.get("unsafe", value.get("flagged", False)))
        categories = [str(x) for x in value.get("categories", [])]
        score = value.get("score")
    else:
        unsafe = bool(getattr(value, "unsafe", getattr(value, "flagged", False)))
        categories = [str(x) for x in getattr(value, "categories", [])]
        score = getattr(value, "score", None)
    return SafetyResult(unsafe=unsafe, categories=categories, score=None if score is None else float(score))
