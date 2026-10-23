"""
vision_models.py - Define local request, response, and normalization helpers
for Static Image and Visual Understanding.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ImageLabel:
    """Represents a detected label or object in an image."""

    name: str
    confidence: float
    parent_names: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "confidence": self.confidence,
            "parent_names": self.parent_names or [],
        }


@dataclass
class ImageDescription:
    """Represents a generated visual description of an image."""

    text: str
    confidence: Optional[float] = None
    model_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "model_id": self.model_id,
        }


@dataclass
class DetectedText:
    """Represents text detected inside an image."""

    text: str
    confidence: float
    bounding_box: Optional[List[float]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"text": self.text, "confidence": self.confidence}
        if self.bounding_box:
            result["bounding_box"] = self.bounding_box
        return result


@dataclass
class SafetyVerdict:
    """Represents a safety or content-policy check result."""

    is_safe: bool
    categories: Dict[str, float] = field(default_factory=dict)
    details: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "categories": self.categories,
            "details": self.details,
        }


@dataclass
class ImageAnalysisResult:
    """Aggregated result from multiple visual analyses."""

    labels: List[ImageLabel] = field(default_factory=list)
    description: Optional[ImageDescription] = None
    detected_texts: List[DetectedText] = field(default_factory=list)
    safety: Optional[SafetyVerdict] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "labels": [l.to_dict() for l in self.labels],
            "description": self.description.to_dict() if self.description else None,
            "detected_texts": [t.to_dict() for t in self.detected_texts],
            "safety": self.safety.to_dict() if self.safety else None,
        }


@dataclass
class SafetyTextVerdict:
    """Result of checking text for unsafe or policy-sensitive content."""

    is_safe: bool
    flags: List[str] = field(default_factory=list)
    details: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "flags": self.flags,
            "details": self.details,
        }


@dataclass
class TranslatedText:
    """Represents a translated text result."""

    original: str
    translated: str
    target_language: str
    source_language: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original": self.original,
            "translated": self.translated,
            "target_language": self.target_language,
            "source_language": self.source_language,
        }


def normalize_label_confidence(raw_confidence) -> float:
    """Normalize a raw confidence value to [0.0, 1.0]."""
    if isinstance(raw_confidence, (int, float)):
        return min(max(float(raw_confidence), 0.0), 1.0)
    return 0.0


def normalize_text_detections(raw_items: List[Dict[str, Any]]) -> List[DetectedText]:
    """Normalize a list of raw text detection items."""
    results = []
    for item in raw_items:
        text = item.get("text", item.get("detectedText", "")).strip()
        if not text:
            continue
        confidence = normalize_label_confidence(
            item.get("confidence", item.get("score", 0.0))
        )
        results.append(DetectedText(text=text, confidence=confidence))
    return results


def normalize_safety_categories(
    raw_categories: Dict[str, Any],
) -> Dict[str, float]:
    """Normalize raw safety/moderation category values to float scores."""
    normalized = {}
    for key, value in raw_categories.items():
        if isinstance(value, dict):
            score = normalize_label_confidence(value.get("Confidence", value.get("score", 0)))
        else:
            score = normalize_label_confidence(value)
        normalized[key] = score
    return normalized
