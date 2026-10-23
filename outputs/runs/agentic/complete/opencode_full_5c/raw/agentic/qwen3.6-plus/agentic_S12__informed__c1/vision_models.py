from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ImageLabel:
    """Represents a detected label or object in an image."""

    name: str
    confidence: float
    bounding_box: Optional[dict] = None


@dataclass
class LabelDetectionRequest:
    """Request payload for image label detection."""

    image_url: str
    max_labels: int = 20
    confidence_threshold: float = 0.5


@dataclass
class LabelDetectionResponse:
    """Response from image label detection."""

    labels: List[ImageLabel] = field(default_factory=list)
    image_url: str = ""
    model: str = ""
    raw_response: Optional[dict] = None


@dataclass
class ImageDescriptionRequest:
    """Request payload for image description."""

    image_url: str
    detail_level: str = "brief"
    language: str = "en"


@dataclass
class ImageDescriptionResponse:
    """Response from image description generation."""

    description: str = ""
    image_url: str = ""
    model: str = ""
    raw_response: Optional[dict] = None


@dataclass
class ImageTextRequest:
    """Request payload for text detection in images (OCR)."""

    image_url: str
    language_hints: Optional[List[str]] = None


@dataclass
class DetectedTextRegion:
    """A region of detected text within an image."""

    text: str
    confidence: float
    bounding_box: Optional[dict] = None
    language: str = ""


@dataclass
class ImageTextResponse:
    """Response from image text detection."""

    regions: List[DetectedTextRegion] = field(default_factory=list)
    full_text: str = ""
    image_url: str = ""
    model: str = ""
    raw_response: Optional[dict] = None


@dataclass
class ImageSafetyRequest:
    """Request payload for image safety scoring."""

    image_url: str
    categories: Optional[List[str]] = None


@dataclass
class SafetyCategoryScore:
    """Score for a single safety category."""

    category: str
    score: float
    label: str = ""


@dataclass
class ImageSafetyResponse:
    """Response from image safety analysis."""

    categories: List[SafetyCategoryScore] = field(default_factory=list)
    overall_safe: bool = True
    image_url: str = ""
    model: str = ""
    raw_response: Optional[dict] = None


def normalize_label_confidence(raw_confidence: float) -> float:
    """Normalize a raw confidence value to [0.0, 1.0]."""
    return max(0.0, min(1.0, raw_confidence))


def normalize_safety_score(raw_score: float) -> float:
    """Normalize a raw safety score to [0.0, 1.0] where higher means more unsafe."""
    return max(0.0, min(1.0, raw_score))


def parse_labels_from_qwen_vl_text(
    text: str, threshold: float = 0.5
) -> List[ImageLabel]:
    """Parse label results from Qwen-VL structured text output."""
    labels = []
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        parts = line.split(":", 1)
        name = parts[0].strip()
        try:
            confidence = float(parts[1].strip())
        except ValueError:
            confidence = 0.5
        if confidence >= threshold:
            labels.append(
                ImageLabel(
                    name=name,
                    confidence=normalize_label_confidence(confidence),
                )
            )
    return labels


def parse_text_regions_from_qwen_vl_text(text: str) -> List[DetectedTextRegion]:
    """Parse OCR text regions from Qwen-VL structured text output."""
    regions = []
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        regions.append(
            DetectedTextRegion(
                text=line,
                confidence=1.0,
            )
        )
    return regions
