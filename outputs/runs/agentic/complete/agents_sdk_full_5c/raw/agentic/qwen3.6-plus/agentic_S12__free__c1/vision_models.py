"""
vision_models.py - Define local request, response, and normalization helpers
for Static Image and Visual Understanding using AWS Rekognition.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class LabelDetectionRequest:
    """Request model for label/object detection in an image."""
    image_bytes: bytes
    min_confidence: float = 50.0
    max_labels: int = 50


@dataclass
class ImageDescriptionRequest:
    """Request model for generating a visual description of an image."""
    image_bytes: bytes
    min_confidence: float = 50.0
    max_description_length: int = 500


@dataclass
class TextDetectionRequest:
    """Request model for detecting text inside an image."""
    image_bytes: bytes
    min_confidence: float = 50.0


@dataclass
class ImageSafetyRequest:
    """Request model for checking image safety/policy content."""
    image_bytes: bytes
    moderation_min_confidence: float = 50.0


@dataclass
class DetectedLabel:
    """Normalized label/object detection result."""
    name: str
    confidence: float
    parents: List[str] = field(default_factory=list)


@dataclass
class DetectedText:
    """Normalized text detection result."""
    text: str
    confidence: float
    bounding_box: Optional[Dict[str, float]] = None


@dataclass
class SafetyFinding:
    """Normalized safety/moderation finding."""
    category: str
    confidence: float
    parent_name: Optional[str] = None


@dataclass
class LabelDetectionResponse:
    """Response wrapper for label detection."""
    labels: List[DetectedLabel]
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class ImageDescriptionResponse:
    """Response wrapper for image description."""
    description: str
    labels_used: List[str] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TextDetectionResponse:
    """Response wrapper for text detection."""
    detected_text: List[DetectedText]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class ImageSafetyResponse:
    """Response wrapper for image safety check."""
    is_safe: bool
    findings: List[SafetyFinding]
    raw_response: Optional[Dict[str, Any]] = None


def normalize_rekognition_labels(rekognition_response: dict, min_confidence: float = 50.0) -> List[DetectedLabel]:
    """Normalize AWS Rekognition DetectLabels response into DetectedLabel objects."""
    labels = []
    for label in rekognition_response.get("Labels", []):
        confidence = label.get("Confidence", 0.0)
        if confidence >= min_confidence:
            parents = [p.get("Name", "") for p in label.get("Parents", [])]
            labels.append(DetectedLabel(
                name=label.get("Name", ""),
                confidence=confidence,
                parents=parents,
            ))
    return labels


def normalize_rekognition_text(rekognition_response: dict, min_confidence: float = 50.0) -> List[DetectedText]:
    """Normalize AWS Rekognition DetectText response into DetectedText objects."""
    texts = []
    for text_item in rekognition_response.get("TextDetections", []):
        if text_item.get("Type") != "LINE":
            continue
        confidence = text_item.get("Confidence", 0.0)
        if confidence >= min_confidence:
            bbox = text_item.get("Geometry", {}).get("BoundingBox", {})
            texts.append(DetectedText(
                text=text_item.get("DetectedText", ""),
                confidence=confidence,
                bounding_box=bbox,
            ))
    return texts


def normalize_rekognition_moderation(rekognition_response: dict, min_confidence: float = 50.0) -> List[SafetyFinding]:
    """Normalize AWS Rekognition DetectModerationLabels response into SafetyFinding objects."""
    findings = []
    for label in rekognition_response.get("ModerationLabels", []):
        confidence = label.get("Confidence", 0.0)
        if confidence >= min_confidence:
            findings.append(SafetyFinding(
                category=label.get("Name", ""),
                confidence=confidence,
                parent_name=label.get("ParentName"),
            ))
    return findings


def build_description_from_labels(labels: List[DetectedLabel], max_length: int = 500) -> str:
    """Build a simple visual description from detected labels."""
    top_labels = sorted(labels, key=lambda l: l.confidence, reverse=True)[:5]
    if not top_labels:
        return "No discernible content detected in the image."
    label_names = [l.name.lower() for l in top_labels]
    description = "The image contains " + ", ".join(label_names) + "."
    if len(description) > max_length:
        description = description[:max_length - 3] + "..."
    return description
