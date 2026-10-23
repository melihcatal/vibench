from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ImageLabelRequest:
    image_path: str
    max_labels: int = 20
    confidence_threshold: float = 0.0


@dataclass
class ImageLabel:
    name: str
    confidence: float
    category: str = ""


@dataclass
class ImageLabelResponse:
    labels: list[ImageLabel] = field(default_factory=list)
    raw_text: str = ""
    image_path: str = ""


@dataclass
class ImageDescriptionRequest:
    image_path: str
    max_length: int = 150
    detail_level: str = "brief"


@dataclass
class ImageDescriptionResponse:
    description: str = ""
    raw_text: str = ""
    image_path: str = ""


@dataclass
class ImageTextRequest:
    image_path: str
    language_hint: str | None = None


@dataclass
class DetectedTextRegion:
    text: str
    bounding_box: dict[str, float] = field(default_factory=dict)
    confidence: float = 1.0
    language: str = ""


@dataclass
class ImageTextResponse:
    regions: list[DetectedTextRegion] = field(default_factory=list)
    full_text: str = ""
    raw_text: str = ""
    image_path: str = ""


@dataclass
class ImageSafetyRequest:
    image_path: str
    categories: list[str] = field(
        default_factory=lambda: [
            "violence",
            "adult",
            "hate",
            "self_harm",
            "illegal",
            "gore",
        ]
    )


@dataclass
class SafetyScore:
    category: str
    score: float
    flagged: bool = False


@dataclass
class ImageSafetyResponse:
    scores: list[SafetyScore] = field(default_factory=list)
    overall_safe: bool = True
    raw_text: str = ""
    image_path: str = ""


def normalize_label_response(raw_text: str, image_path: str) -> ImageLabelResponse:
    import json

    labels: list[ImageLabel] = []
    try:
        data = json.loads(raw_text)
        items = data if isinstance(data, list) else data.get("labels", [])
        for item in items:
            labels.append(
                ImageLabel(
                    name=item.get("name", item.get("label", "")),
                    confidence=float(item.get("confidence", item.get("score", 0.0))),
                    category=item.get("category", ""),
                )
            )
    except (json.JSONDecodeError, KeyError, ValueError):
        for line in raw_text.strip().splitlines():
            line = line.strip()
            if line:
                parts = line.rsplit(":", 1)
                name = parts[0].strip() if parts else line
                conf = float(parts[1].strip()) if len(parts) > 1 else 0.5
                labels.append(ImageLabel(name=name, confidence=conf))
    return ImageLabelResponse(labels=labels, raw_text=raw_text, image_path=image_path)


def normalize_description_response(
    raw_text: str, image_path: str
) -> ImageDescriptionResponse:
    return ImageDescriptionResponse(
        description=raw_text.strip(),
        raw_text=raw_text,
        image_path=image_path,
    )


def normalize_text_response(raw_text: str, image_path: str) -> ImageTextResponse:
    import json

    regions: list[DetectedTextRegion] = []
    full_text_parts: list[str] = []
    try:
        data = json.loads(raw_text)
        items = (
            data
            if isinstance(data, list)
            else data.get("text_regions", data.get("regions", []))
        )
        for item in items:
            text = item.get("text", "")
            full_text_parts.append(text)
            regions.append(
                DetectedTextRegion(
                    text=text,
                    bounding_box=item.get("bounding_box", {}),
                    confidence=float(item.get("confidence", 1.0)),
                    language=item.get("language", ""),
                )
            )
    except (json.JSONDecodeError, KeyError, ValueError):
        full_text_parts = [raw_text.strip()]
        regions.append(DetectedTextRegion(text=raw_text.strip()))
    return ImageTextResponse(
        regions=regions,
        full_text=" ".join(full_text_parts).strip(),
        raw_text=raw_text,
        image_path=image_path,
    )


def normalize_safety_response(raw_text: str, image_path: str) -> ImageSafetyResponse:
    import json

    scores: list[SafetyScore] = []
    overall_safe = True
    try:
        data = json.loads(raw_text)
        items = (
            data
            if isinstance(data, list)
            else data.get("scores", data.get("categories", []))
        )
        for item in items:
            cat = item.get("category", item.get("name", ""))
            score = float(item.get("score", item.get("confidence", 0.0)))
            flagged = bool(item.get("flagged", score > 0.7))
            if flagged:
                overall_safe = False
            scores.append(SafetyScore(category=cat, score=score, flagged=flagged))
    except (json.JSONDecodeError, KeyError, ValueError):
        for line in raw_text.strip().splitlines():
            line = line.strip()
            if ":" in line:
                cat, val = line.split(":", 1)
                try:
                    score = float(val.strip())
                except ValueError:
                    score = 0.0
                flagged = score > 0.7
                if flagged:
                    overall_safe = False
                scores.append(
                    SafetyScore(category=cat.strip(), score=score, flagged=flagged)
                )
    return ImageSafetyResponse(
        scores=scores,
        overall_safe=overall_safe,
        raw_text=raw_text,
        image_path=image_path,
    )
