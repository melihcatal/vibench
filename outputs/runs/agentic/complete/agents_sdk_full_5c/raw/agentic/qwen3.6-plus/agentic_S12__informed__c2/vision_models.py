"""
vision_models.py - Local request, response, and normalization helpers
for Static Image and Visual Understanding with Azure AI Vision.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ImageRequest:
    """Normalized input request for image analysis operations."""
    image_path: str
    language: str = "en"
    features: List[str] = field(default_factory=list)
    confidence_threshold: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image_path": self.image_path,
            "language": self.language,
            "features": self.features,
            "confidence_threshold": self.confidence_threshold,
        }


@dataclass
class DetectedLabel:
    """Represents a single detected label or object in an image."""
    name: str
    confidence: float
    bounding_box: Optional[Dict[str, int]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"name": self.name, "confidence": self.confidence}
        if self.bounding_box:
            result["bounding_box"] = self.bounding_box
        return result


@dataclass
class ImageDescription:
    """Represents a generated visual description of an image."""
    text: str
    confidence: float
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "tags": self.tags,
        }


@dataclass
class DetectedTextRegion:
    """Represents a region of detected text inside an image."""
    text: str
    confidence: float
    bounding_box: Optional[List[int]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"text": self.text, "confidence": self.confidence}
        if self.bounding_box:
            result["bounding_box"] = self.bounding_box
        return result


@dataclass
class SafetyScore:
    """Represents safety or policy-sensitive content assessment."""
    is_safe: bool
    categories: Dict[str, float] = field(default_factory=dict)
    reasons: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "categories": self.categories,
            "reasons": self.reasons,
        }


@dataclass
class VisionAnalysisResponse:
    """Aggregated response container for all vision analysis results."""
    labels: List[DetectedLabel] = field(default_factory=list)
    description: Optional[ImageDescription] = None
    text_regions: List[DetectedTextRegion] = field(default_factory=list)
    safety: Optional[SafetyScore] = None
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.labels:
            result["labels"] = [label.to_dict() for label in self.labels]
        if self.description:
            result["description"] = self.description.to_dict()
        if self.text_regions:
            result["text_regions"] = [t.to_dict() for t in self.text_regions]
        if self.safety:
            result["safety"] = self.safety.to_dict()
        if self.raw_response:
            result["raw_response"] = self.raw_response
        return result


def normalize_label_from_azure(raw_label: Any) -> DetectedLabel:
    """Normalize an Azure AI Vision label result into a DetectedLabel."""
    name = getattr(raw_label, "name", "") or ""
    confidence = getattr(raw_label, "confidence", 0.0) or 0.0
    return DetectedLabel(name=name, confidence=float(confidence))


def normalize_description_from_azure(raw_caption: Any) -> ImageDescription:
    """Normalize an Azure AI Vision caption into an ImageDescription."""
    text = getattr(raw_caption, "text", "") or ""
    confidence = getattr(raw_caption, "confidence", 0.0) or 0.0
    tags = getattr(raw_caption, "tags", []) or []
    return ImageDescription(
        text=str(text),
        confidence=float(confidence),
        tags=[str(t) for t in tags],
    )


def normalize_text_region_from_azure(raw_word: Any) -> DetectedTextRegion:
    """Normalize an Azure AI Vision OCR word into a DetectedTextRegion."""
    text = getattr(raw_word, "text", "") or ""
    confidence = getattr(raw_word, "confidence", 0.0) or 0.0
    bounding_box = getattr(raw_word, "bounding_box", None)
    box = None
    if bounding_box is not None:
        box = [int(getattr(bounding_box, attr, 0)) for attr in ("x", "y", "w", "h")]
    return DetectedTextRegion(text=str(text), confidence=float(confidence), bounding_box=box)


def normalize_safety_from_azure(raw_result: Any) -> SafetyScore:
    """Normalize Azure AI Vision moderation result into a SafetyScore."""
    categories: Dict[str, float] = {}
    reasons: List[str] = []
    is_safe = True

    moderation = getattr(raw_result, "result", None)
    if moderation is not None:
        for cat in ("adult", "racy", "gore", "hate", "selfHarm", "violence"):
            score = getattr(moderation, cat, None)
            if score is not None:
                categories[cat] = float(score)
                if float(score) > 0.5:
                    is_safe = False
                    reasons.append(cat)

    return SafetyScore(is_safe=is_safe, categories=categories, reasons=reasons)
