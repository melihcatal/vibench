from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ImageInput:
    image_path: str | None = None
    image_url: str | None = None


@dataclass
class LabelDetectionResult:
    provider: str
    labels: list[dict[str, Any]] = field(default_factory=list)
    raw_response: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImageDescriptionResult:
    provider: str
    description: str
    raw_response: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TextDetectionResult:
    provider: str
    text: str
    blocks: list[dict[str, Any]] = field(default_factory=list)
    raw_response: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImageSafetyResult:
    provider: str
    safe: bool
    categories: list[dict[str, Any]] = field(default_factory=list)
    raw_response: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImageSummaryResult:
    provider: str
    summary: str
    raw_response: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    target_language: str
    raw_response: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TextSafetyResult:
    provider: str
    safe: bool
    scores: dict[str, Any] = field(default_factory=dict)
    raw_response: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ArchiveResult:
    provider: str
    bucket: str
    object_key: str
    uri: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_rekognition_labels(response: dict[str, Any]) -> list[dict[str, Any]]:
    labels = []
    for item in response.get("Labels", []):
        labels.append(
            {
                "name": item.get("Name"),
                "confidence": item.get("Confidence"),
                "parents": [parent.get("Name") for parent in item.get("Parents", [])],
                "aliases": [alias.get("Name") for alias in item.get("Aliases", [])],
                "categories": [
                    category.get("Name") for category in item.get("Categories", [])
                ],
            }
        )
    return labels


def normalize_rekognition_text(
    response: dict[str, Any],
) -> tuple[str, list[dict[str, Any]]]:
    blocks = []
    lines = []
    for item in response.get("TextDetections", []):
        entry = {
            "type": item.get("Type"),
            "text": item.get("DetectedText"),
            "confidence": item.get("Confidence"),
        }
        blocks.append(entry)
        if item.get("Type") == "LINE" and item.get("DetectedText"):
            lines.append(item["DetectedText"])
    return "\n".join(lines), blocks


def normalize_rekognition_safety(
    response: dict[str, Any], threshold: float = 60.0
) -> ImageSafetyResult:
    categories = []
    unsafe = False
    for item in response.get("ModerationLabels", []):
        confidence = float(item.get("Confidence", 0.0))
        categories.append(
            {
                "name": item.get("Name"),
                "parent_name": item.get("ParentName"),
                "confidence": confidence,
                "taxonomy_level": item.get("TaxonomyLevel"),
            }
        )
        if confidence >= threshold:
            unsafe = True
    return ImageSafetyResult(
        provider="amazon-rekognition",
        safe=not unsafe,
        categories=categories,
        raw_response=response,
    )


def compact_analysis_payload(data: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in data.items() if value not in (None, [], {}, "")
    }
