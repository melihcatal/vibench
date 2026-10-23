from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageSource:
    image_bytes: Optional[bytes] = None
    image_url: Optional[str] = None
    mime_type: str = "image/jpeg"


@dataclass
class LabelDetectionResult:
    provider: str
    labels: List[str]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImageDescriptionResult:
    provider: str
    description: str
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TextDetectionResult:
    provider: str
    text: str
    lines: List[str]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyScoreResult:
    provider: str
    safe: bool
    categories: Dict[str, float]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualSummaryResult:
    provider: str
    summary: str
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    target_language: str
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UnsafeTextCheckResult:
    provider: str
    flagged: bool
    categories: Dict[str, bool]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ArchiveResult:
    provider: str
    bucket: str
    object_key: str
    uri: str


def image_to_data_uri(image: ImageSource) -> str:
    import base64

    if image.image_url:
        return image.image_url
    if not image.image_bytes:
        raise ValueError("image_bytes or image_url is required")
    encoded = base64.b64encode(image.image_bytes).decode("utf-8")
    return f"data:{image.mime_type};base64,{encoded}"


def normalize_labels(items: List[str], limit: int = 10) -> List[str]:
    seen = set()
    normalized: List[str] = []
    for item in items:
        value = item.strip()
        if value and value.lower() not in seen:
            seen.add(value.lower())
            normalized.append(value)
        if len(normalized) >= limit:
            break
    return normalized


def flatten_text_lines(text: str) -> List[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]
