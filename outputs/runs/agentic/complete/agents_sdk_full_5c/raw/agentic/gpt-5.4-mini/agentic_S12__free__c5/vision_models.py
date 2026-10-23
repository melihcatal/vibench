from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class Label:
    description: str
    score: float


@dataclass(frozen=True)
class ImageLabelResult:
    labels: List[Label]


@dataclass(frozen=True)
class OCRResult:
    text: str
    words: List[str]


@dataclass(frozen=True)
class SafetyScore:
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


def coerce_labels(items: Iterable[Dict[str, Any]]) -> ImageLabelResult:
    labels = [Label(description=str(item.get("description", "")), score=float(item.get("score", 0.0))) for item in items]
    return ImageLabelResult(labels=labels)


def coerce_ocr(items: List[Dict[str, Any]]) -> OCRResult:
    text = items[0].get("description", "") if items else ""
    words = [item.get("description", "") for item in items[1:]] if len(items) > 1 else []
    return OCRResult(text=text, words=words)


def coerce_safety(item: Dict[str, Any]) -> SafetyScore:
    return SafetyScore(
        adult=str(item.get("adult", "UNKNOWN")),
        spoof=str(item.get("spoof", "UNKNOWN")),
        medical=str(item.get("medical", "UNKNOWN")),
        violence=str(item.get("violence", "UNKNOWN")),
        racy=str(item.get("racy", "UNKNOWN")),
    )


def image_description_from_google_vision(data: Dict[str, Any]) -> str:
    responses = data.get("responses", [{}])
    props = responses[0].get("imagePropertiesAnnotation", {}) if responses else {}
    colors = props.get("dominantColors", {}).get("colors", [])
    if not colors:
        return "A visually rich image with varied colors."
    top = colors[0].get("color", {})
    return f"An image dominated by RGB({top.get('red', 0)}, {top.get('green', 0)}, {top.get('blue', 0)})."


__all__ = [
    "Label",
    "ImageLabelResult",
    "OCRResult",
    "SafetyScore",
    "coerce_labels",
    "coerce_ocr",
    "coerce_safety",
    "image_description_from_google_vision",
]
