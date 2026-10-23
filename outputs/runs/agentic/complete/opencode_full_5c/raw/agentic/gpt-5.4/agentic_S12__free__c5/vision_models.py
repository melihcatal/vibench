from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageInput:
    image_bytes: bytes
    mime_type: str = "image/jpeg"
    source_name: Optional[str] = None


@dataclass
class LabelDetectionResult:
    provider: str
    labels: List[Dict[str, Any]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImageDescriptionResult:
    provider: str
    description: str
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImageTextDetectionResult:
    provider: str
    text: str
    lines: List[str] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImageSafetyResult:
    provider: str
    flagged: bool
    categories: Dict[str, Any] = field(default_factory=dict)
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualAnalysisBundle:
    labels: List[Dict[str, Any]] = field(default_factory=list)
    description: str = ""
    detected_text: str = ""
    safety_categories: Dict[str, Any] = field(default_factory=dict)


def normalize_google_vision_labels(response: Dict[str, Any]) -> LabelDetectionResult:
    labels: List[Dict[str, Any]] = []
    for item in response.get("labelAnnotations", []) or []:
        labels.append(
            {
                "name": item.get("description", ""),
                "score": item.get("score", 0.0),
                "mid": item.get("mid"),
                "topicality": item.get("topicality"),
            }
        )
    for item in response.get("localizedObjectAnnotations", []) or []:
        labels.append(
            {
                "name": item.get("name", ""),
                "score": item.get("score", 0.0),
                "mid": item.get("mid"),
                "bounding_poly": item.get("boundingPoly", {}),
            }
        )
    return LabelDetectionResult(
        provider="google-cloud-vision", labels=labels, raw_response=response
    )


def normalize_openai_description(response: Dict[str, Any]) -> ImageDescriptionResult:
    text = ""
    for output in response.get("output", []) or []:
        for content in output.get("content", []) or []:
            if content.get("type") == "output_text":
                text += content.get("text", "")
    return ImageDescriptionResult(
        provider="openai", description=text.strip(), raw_response=response
    )


def normalize_google_vision_text(response: Dict[str, Any]) -> ImageTextDetectionResult:
    annotations = response.get("textAnnotations", []) or []
    full_text = annotations[0].get("description", "") if annotations else ""
    lines = [line for line in full_text.splitlines() if line.strip()]
    return ImageTextDetectionResult(
        provider="google-cloud-vision",
        text=full_text,
        lines=lines,
        raw_response=response,
    )


def normalize_openai_moderation(response: Dict[str, Any]) -> ImageSafetyResult:
    results = response.get("results", []) or []
    result = results[0] if results else {}
    categories = result.get("categories", {}) or {}
    return ImageSafetyResult(
        provider="openai",
        flagged=bool(result.get("flagged", False)),
        categories=categories,
        raw_response=response,
    )


def build_visual_summary_payload(bundle: VisualAnalysisBundle) -> Dict[str, Any]:
    return {
        "labels": bundle.labels,
        "description": bundle.description,
        "detected_text": bundle.detected_text,
        "safety_categories": bundle.safety_categories,
    }
