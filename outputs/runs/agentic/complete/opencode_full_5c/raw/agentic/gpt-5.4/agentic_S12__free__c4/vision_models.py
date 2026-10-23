from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageInput:
    image_bytes: bytes
    mime_type: str = "image/jpeg"
    source_uri: Optional[str] = None


@dataclass
class LabelDetectionResult:
    provider: str
    labels: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ImageDescriptionResult:
    provider: str
    description: str
    model: str


@dataclass
class ImageTextResult:
    provider: str
    text: str
    blocks: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ImageSafetyResult:
    provider: str
    safe: bool
    categories: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ImageSummaryResult:
    provider: str
    summary: str
    model: str


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    target_language: str


@dataclass
class VisualSafetyTextResult:
    provider: str
    flagged: bool
    categories: List[str] = field(default_factory=list)


@dataclass
class ArchiveResult:
    provider: str
    bucket: str
    object_key: str
    url: str


def normalize_google_vision_labels(response: Any) -> LabelDetectionResult:
    labels = []
    for item in getattr(response, "label_annotations", []) or []:
        labels.append(
            {
                "name": getattr(item, "description", ""),
                "score": float(getattr(item, "score", 0.0) or 0.0),
                "mid": getattr(item, "mid", ""),
            }
        )
    for item in getattr(response, "localized_object_annotations", []) or []:
        labels.append(
            {
                "name": getattr(item, "name", ""),
                "score": float(getattr(item, "score", 0.0) or 0.0),
                "mid": getattr(item, "mid", ""),
            }
        )
    return LabelDetectionResult(provider="google-cloud-vision", labels=labels)


def normalize_google_vision_text(response: Any) -> ImageTextResult:
    blocks: List[Dict[str, Any]] = []
    annotations = getattr(response, "text_annotations", []) or []
    full_text = annotations[0].description if annotations else ""
    for item in annotations[1:]:
        vertices = []
        polygon = getattr(item, "bounding_poly", None)
        for vertex in getattr(polygon, "vertices", []) or []:
            vertices.append(
                {"x": getattr(vertex, "x", 0), "y": getattr(vertex, "y", 0)}
            )
        blocks.append(
            {
                "text": getattr(item, "description", ""),
                "vertices": vertices,
            }
        )
    return ImageTextResult(
        provider="google-cloud-vision", text=full_text, blocks=blocks
    )


def normalize_google_safe_search(response: Any) -> ImageSafetyResult:
    safe_search = getattr(response, "safe_search_annotation", None)
    categories = []
    if safe_search:
        for name in ["adult", "spoof", "medical", "violence", "racy"]:
            categories.append(
                {"name": name, "likelihood": str(getattr(safe_search, name, "UNKNOWN"))}
            )
    unsafe_values = {"LIKELY", "VERY_LIKELY"}
    safe = not any(category["likelihood"] in unsafe_values for category in categories)
    return ImageSafetyResult(
        provider="google-cloud-vision", safe=safe, categories=categories
    )


def normalize_storage_key(image_name: str, suffix: str) -> str:
    base = image_name.rsplit(".", 1)[0]
    return f"{base}-{suffix}.json"
