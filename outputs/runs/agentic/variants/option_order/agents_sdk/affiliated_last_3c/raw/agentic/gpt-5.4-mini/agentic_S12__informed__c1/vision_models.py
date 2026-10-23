from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Sequence


@dataclass(frozen=True)
class ImageInput:
    image_uri: str | None = None
    image_path: str | None = None
    image_bytes: bytes | None = None
    content_type: str | None = None


@dataclass(frozen=True)
class VisionRequest:
    image: ImageInput
    language: str | None = None
    max_results: int = 10


@dataclass(frozen=True)
class VisionItem:
    name: str
    confidence: float | None = None
    description: str | None = None
    bounding_box: Dict[str, Any] | None = None


@dataclass(frozen=True)
class VisionTextResult:
    text: str
    confidence: float | None = None


@dataclass(frozen=True)
class VisionSafetyResult:
    safe: bool
    categories: Dict[str, float]
    reason: str | None = None


def normalize_items(items: Iterable[Mapping[str, Any]]) -> List[VisionItem]:
    normalized: List[VisionItem] = []
    for item in items:
        normalized.append(
            VisionItem(
                name=str(item.get("name") or item.get("label") or item.get("text") or "unknown"),
                confidence=_to_float(item.get("confidence") or item.get("score")),
                description=item.get("description"),
                bounding_box=item.get("bounding_box") or item.get("boundingBox"),
            )
        )
    return normalized


def _to_float(value: Any) -> float | None:
    try:
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None


def image_payload_from_input(image: ImageInput) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    if image.image_uri:
        payload["image_uri"] = image.image_uri
    if image.image_path:
        payload["image_path"] = image.image_path
    if image.image_bytes is not None:
        payload["image_bytes"] = image.image_bytes
    if image.content_type:
        payload["content_type"] = image.content_type
    return payload
