from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ImageInput:
    image_path: str | None = None
    image_bytes: bytes | None = None
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
    raw_response: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TextDetectionResult:
    provider: str
    text: str
    blocks: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SafetyScoreResult:
    provider: str
    safe: bool
    scores: dict[str, float] = field(default_factory=dict)
    flagged_categories: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class VisualAnalysisBundle:
    labels: list[dict[str, Any]] = field(default_factory=list)
    description: str = ""
    detected_text: str = ""
    safety: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_rekognition_labels(response: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "name": item.get("Name", ""),
            "confidence": float(item.get("Confidence", 0.0)),
            "parents": [parent.get("Name", "") for parent in item.get("Parents", [])],
        }
        for item in response.get("Labels", [])
    ]


def normalize_rekognition_text(
    response: dict[str, Any],
) -> tuple[str, list[dict[str, Any]]]:
    blocks = [
        {
            "type": block.get("Type", ""),
            "text": block.get("DetectedText", ""),
            "confidence": float(block.get("Confidence", 0.0)),
        }
        for block in response.get("TextDetections", [])
        if block.get("DetectedText")
    ]
    combined = "\n".join(block["text"] for block in blocks if block["type"] == "LINE")
    return combined, blocks


def normalize_rekognition_moderation(
    response: dict[str, Any], threshold: float
) -> dict[str, Any]:
    scores: dict[str, float] = {}
    flagged: list[str] = []
    for item in response.get("ModerationLabels", []):
        name = item.get("Name", "")
        confidence = float(item.get("Confidence", 0.0))
        scores[name] = confidence
        if confidence >= threshold:
            flagged.append(name)
    return {
        "safe": len(flagged) == 0,
        "scores": scores,
        "flagged_categories": flagged,
    }
