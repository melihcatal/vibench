"""
Local request, response, and normalization helpers for Static Image and Visual Understanding.
Defines dataclasses and utilities for working with Google Cloud Vision API responses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from google.cloud.vision_v1 import Feature
from google.cloud.vision_v1.types import (
    EntityAnnotation,
    ImageProperties,
    SafeSearchAnnotation,
    TextAnnotation,
)


@dataclass
class LabelResult:
    """Represents detected labels or objects in an image."""

    label: str
    confidence: float
    mid: Optional[str] = None
    topicality: Optional[float] = None
    bounding_poly: Optional[dict] = None

    @classmethod
    def from_entity(cls, entity: EntityAnnotation) -> LabelResult:
        """Create LabelResult from a Google Cloud Vision EntityAnnotation."""
        bounding = None
        if entity.bounding_poly:
            bounding = {
                "vertices": [
                    {"x": v.x, "y": v.y} for v in entity.bounding_poly.vertices
                ]
            }
        return cls(
            label=entity.description,
            confidence=entity.score or 0.0,
            mid=entity.mid,
            topicality=getattr(entity, "topicality", None),
            bounding_poly=bounding,
        )


@dataclass
class ImageDescription:
    """Represents a generated visual description for an image."""

    description: str
    confidence: float
    locale: Optional[str] = None

    @classmethod
    def from_entity(cls, entity: EntityAnnotation) -> ImageDescription:
        """Create ImageDescription from a Google Cloud Vision EntityAnnotation."""
        return cls(
            description=entity.description,
            confidence=entity.score or 0.0,
            locale=entity.locale,
        )


@dataclass
class DetectedText:
    """Represents detected text appearing inside an image."""

    text: str
    confidence: float
    language: Optional[str] = None
    bounding_poly: Optional[dict] = None

    @classmethod
    def from_entity(cls, entity: EntityAnnotation) -> DetectedText:
        """Create DetectedText from a Google Cloud Vision EntityAnnotation."""
        bounding = None
        if entity.bounding_poly:
            bounding = {
                "vertices": [
                    {"x": v.x, "y": v.y} for v in entity.bounding_poly.vertices
                ]
            }
        return cls(
            text=entity.description,
            confidence=entity.score or 0.0,
            language=entity.locale,
            bounding_poly=bounding,
        )


@dataclass
class SafetyScores:
    """Represents safety/policy scores for visual content."""

    adult: str = "UNKNOWN"
    spoof: str = "UNKNOWN"
    medical: str = "UNKNOWN"
    violence: str = "UNKNOWN"
    racy: str = "UNKNOWN"

    adult_confidence: Optional[float] = None
    spoof_confidence: Optional[float] = None
    medical_confidence: Optional[float] = None
    violence_confidence: Optional[float] = None
    racy_confidence: Optional[float] = None

    @classmethod
    def from_safe_search(cls, safe: SafeSearchAnnotation) -> SafetyScores:
        """Create SafetyScores from a Google Cloud Vision SafeSearchAnnotation."""
        return cls(
            adult=safe.adult.name,
            spoof=safe.spoof.name,
            medical=safe.medical.name,
            violence=safe.violence.name,
            racy=safe.racy.name,
            adult_confidence=safe.adult_confidence,
            spoof_confidence=safe.spoof_confidence,
            medical_confidence=safe.medical_confidence,
            violence_confidence=safe.violence_confidence,
            racy_confidence=safe.racy_confidence,
        )

    def is_unsafe(self, threshold: str = "POSSIBLE") -> bool:
        """
        Check if any category meets or exceeds the unsafe threshold.

        Args:
            threshold: Minimum likelihood level to consider unsafe.
                       One of: VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY.

        Returns:
            True if any category is at or above threshold.
        """
        levels = ["UNKNOWN", "VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]
        threshold_idx = levels.index(threshold) if threshold in levels else 3
        for attr in ["adult", "spoof", "medical", "violence", "racy"]:
            val = getattr(self, attr, "UNKNOWN")
            if val in levels and levels.index(val) >= threshold_idx:
                return True
        return False


@dataclass
class VisionAnalysisResponse:
    """Consolidated response container for vision analysis results."""

    image_source: str
    labels: list[LabelResult] = field(default_factory=list)
    descriptions: list[ImageDescription] = field(default_factory=list)
    detected_texts: list[DetectedText] = field(default_factory=list)
    safety: Optional[SafetyScores] = None
    errors: list[str] = field(default_factory=list)


def get_label_detection_feature(max_results: int = 10) -> Feature:
    """Create a Feature object for label detection."""
    return Feature(type_=Feature.Type.LABEL_DETECTION, max_results=max_results)


def get_web_detection_feature(max_results: int = 10) -> Feature:
    """Create a Feature object for web detection (includes image properties)."""
    return Feature(type_=Feature.Type.WEB_DETECTION, max_results=max_results)


def get_text_detection_feature() -> Feature:
    """Create a Feature object for text detection (OCR)."""
    return Feature(type_=Feature.Type.TEXT_DETECTION)


def get_document_text_detection_feature() -> Feature:
    """Create a Feature object for dense document text detection."""
    return Feature(type_=Feature.Type.DOCUMENT_TEXT_DETECTION)


def get_image_properties_feature(max_colors: int = 10) -> Feature:
    """Create a Feature object for image properties (dominant colors)."""
    return Feature(
        type_=Feature.Type.IMAGE_PROPERTIES,
        image_properties_context=Feature.ImagePropertiesContext(
            max_colors=max_colors
        ),
    )


def get_safe_search_detection_feature() -> Feature:
    """Create a Feature object for SafeSearch detection."""
    return Feature(type_=Feature.Type.SAFE_SEARCH_DETECTION)


def get_logo_detection_feature() -> Feature:
    """Create a Feature object for logo detection."""
    return Feature(type_=Feature.Type.LOGO_DETECTION)


def get_face_detection_feature() -> Feature:
    """Create a Feature object for face detection."""
    return Feature(type_=Feature.Type.FACE_DETECTION)


def get_landmark_detection_feature() -> Feature:
    """Create a Feature object for landmark detection."""
    return Feature(type_=Feature.Type.LANDMARK_DETECTION)


def get_object_localization_feature() -> Feature:
    """Create a Feature object for object localization."""
    return Feature(type_=Feature.Type.OBJECT_LOCALIZATION)
