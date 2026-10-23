from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ImageSource:
    image_bytes: bytes | None = None
    image_uri: str | None = None


@dataclass
class LabelDetectionResult:
    labels: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImageDescriptionResult:
    description: str
    model: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImageTextDetectionResult:
    text: str
    blocks: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImageSafetyResult:
    safe: bool
    categories: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_labels(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for item in items:
        normalized.append(
            {
                "name": item.get("name") or item.get("Name") or "",
                "confidence": float(
                    item.get("confidence") or item.get("Confidence") or 0.0
                ),
            }
        )
    return normalized


def normalize_text_blocks(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for item in items:
        normalized.append(
            {
                "text": item.get("text") or item.get("DetectedText") or "",
                "kind": item.get("kind") or item.get("Type") or "",
                "confidence": float(
                    item.get("confidence") or item.get("Confidence") or 0.0
                ),
            }
        )
    return normalized


def compact_text(items: list[dict[str, Any]]) -> str:
    parts = [
        str(item.get("text", "")).strip()
        for item in items
        if str(item.get("text", "")).strip()
    ]
    return "\n".join(parts)
