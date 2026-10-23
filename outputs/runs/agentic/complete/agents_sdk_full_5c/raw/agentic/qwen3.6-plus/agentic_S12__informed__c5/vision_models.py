"""
Local request, response, and normalization helpers for Static Image and Visual Understanding.

Provides unified model definitions and payload/response normalization
across multiple visual analysis providers.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

@dataclass
class ImageAnalysisRequest:
    """Unified request model for image analysis operations."""
    image_source: str  # file path, URL, or base64 string
    features: List[str] = field(default_factory=list)
    language: str = "en"
    confidence_threshold: float = 0.5
    max_results: int = 50
    custom_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LabelDetectionRequest:
    """Request model for label/object detection in images."""
    image_source: str
    max_labels: int = 50
    min_confidence: float = 0.5
    custom_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImageDescriptionRequest:
    """Request model for image description/caption generation."""
    image_source: str
    max_descriptions: int = 5
    language: str = "en"
    detail_level: str = "medium"  # low, medium, high
    custom_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TextDetectionRequest:
    """Request model for text/OCR detection in images."""
    image_source: str
    language_hints: List[str] = field(default_factory=lambda: ["en"])
    detect_orientation: bool = True
    custom_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyModerationRequest:
    """Request model for image safety/content moderation."""
    image_source: str
    categories: Optional[List[str]] = None
    min_confidence: float = 0.5
    custom_params: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------

@dataclass
class DetectedLabel:
    """Represents a detected label or object in an image."""
    name: str
    confidence: float
    parents: List[str] = field(default_factory=list)
    instances: List[Dict[str, Any]] = field(default_factory=list)
    bounding_box: Optional[Dict[str, float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImageDescription:
    """Represents a generated visual description for an image."""
    text: str
    confidence: float
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DetectedText:
    """Represents a detected text region in an image."""
    text: str
    confidence: float
    bounding_box: Optional[Dict[str, float]] = None
    line_number: Optional[int] = None
    word_indices: Optional[List[int]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyCategory:
    """Represents a safety/moderation category with a confidence score."""
    category: str
    confidence: float
    label: str = ""  # e.g., "SAFE", "UNSAFE", "POSSIBLY_UNSAFE"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LabelDetectionResponse:
    """Normalized response for label detection."""
    labels: List[DetectedLabel]
    label_model_version: str = ""
    request_id: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class ImageDescriptionResponse:
    """Normalized response for image description."""
    descriptions: List[ImageDescription]
    tags: List[str] = field(default_factory=list)
    request_id: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TextDetectionResponse:
    """Normalized response for text/OCR detection."""
    detected_texts: List[DetectedText]
    orientation_correction: int = 0
    text_model_version: str = ""
    request_id: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class SafetyModerationResponse:
    """Normalized response for safety moderation."""
    moderation_labels: List[SafetyCategory]
    is_safe: bool = True
    highest_severity: str = "NONE"
    request_id: str = ""
    raw_response: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------

def normalize_rekognition_labels(raw_response: Dict[str, Any]) -> List[DetectedLabel]:
    """Normalize Amazon Rekognition label detection response."""
    labels = []
    for item in raw_response.get("Labels", []):
        parents = [p.get("Name", "") for p in item.get("Parents", [])]
        instances = []
        for inst in item.get("Instances", []):
            box = inst.get("BoundingBox", {})
            instances.append({
                "bounding_box": box,
                "confidence": inst.get("Confidence", 0.0),
            })
        labels.append(DetectedLabel(
            name=item.get("Name", ""),
            confidence=item.get("Confidence", 0.0),
            parents=parents,
            instances=instances,
        ))
    return labels


def normalize_rekognition_text(raw_response: Dict[str, Any]) -> List[DetectedText]:
    """Normalize Amazon Rekognition text detection response."""
    texts = []
    for item in raw_response.get("TextDetections", []):
        detection_type = item.get("Type", "LINE")
        if detection_type != "LINE":
            continue
        box = item.get("Geometry", {}).get("BoundingBox", {})
        texts.append(DetectedText(
            text=item.get("DetectedText", ""),
            confidence=item.get("Confidence", 0.0),
            bounding_box={
                "left": box.get("Left", 0),
                "top": box.get("Top", 0),
                "width": box.get("Width", 0),
                "height": box.get("Height", 0),
            },
        ))
    return texts


def normalize_rekognition_moderation(raw_response: Dict[str, Any]) -> List[SafetyCategory]:
    """Normalize Amazon Rekognition moderation labels response."""
    categories = []
    for item in raw_response.get("ModerationLabels", []):
        categories.append(SafetyCategory(
            category=item.get("Name", ""),
            confidence=item.get("Confidence", 0.0),
            label=item.get("ParentName", ""),
            metadata={
                "taxonomy_level": item.get("TaxonomyLevel", ""),
            },
        ))
    return categories


def filter_by_confidence(
    items: List[Any],
    threshold: float,
    attr: str = "confidence",
) -> List[Any]:
    """Filter a list of items by a confidence attribute threshold."""
    return [item for item in items if getattr(item, attr, 0.0) >= threshold]
