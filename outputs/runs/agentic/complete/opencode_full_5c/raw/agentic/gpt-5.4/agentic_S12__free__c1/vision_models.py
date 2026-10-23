from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ImageInput:
    image_bytes: bytes | None = None
    image_uri: str | None = None
    mime_type: str = "image/jpeg"


@dataclass
class LabelDetectionResult:
    provider: str
    labels: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImageDescriptionResult:
    provider: str
    description: str
    model: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImageTextDetectionResult:
    provider: str
    text: str
    lines: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImageSafetyResult:
    provider: str
    safe: bool
    categories: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImageAnalysisBundle:
    labels: list[dict[str, Any]] = field(default_factory=list)
    description: str = ""
    detected_text: str = ""
    safety: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SummaryResult:
    provider: str
    summary: str
    model: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    target_language: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class UnsafeTextCheckResult:
    provider: str
    flagged: bool
    categories: list[str] = field(default_factory=list)
    model: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ArchiveResult:
    provider: str
    bucket: str
    key: str
    uri: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_labels(labels: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for item in labels:
        normalized.append(
            {
                "name": item.get("name") or item.get("label") or "",
                "score": float(item.get("score", 0.0)),
            }
        )
    return normalized


def compact_analysis_payload(
    analysis: ImageAnalysisBundle | dict[str, Any],
) -> dict[str, Any]:
    payload = (
        analysis.to_dict()
        if isinstance(analysis, ImageAnalysisBundle)
        else dict(analysis)
    )
    payload["labels"] = normalize_labels(payload.get("labels", []))
    return payload
