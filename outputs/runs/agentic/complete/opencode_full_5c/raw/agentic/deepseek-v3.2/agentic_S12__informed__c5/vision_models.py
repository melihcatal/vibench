from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SafetyLevel(Enum):
    """Safety level enumeration."""

    UNKNOWN = "UNKNOWN"
    VERY_UNLIKELY = "VERY_UNLIKELY"
    UNLIKELY = "UNLIKELY"
    POSSIBLE = "POSSIBLE"
    LIKELY = "LIKELY"
    VERY_LIKELY = "VERY_LIKELY"


@dataclass
class ImageLabel:
    """Image label/object detection result."""

    description: str
    score: float
    mid: str


@dataclass
class TextDetection:
    """Text detection result."""

    text: str
    bounds: List[tuple]


@dataclass
class ImageText:
    """Full image text detection result."""

    full_text: str
    text_blocks: List[TextDetection]


@dataclass
class SafetyScores:
    """Image safety scores."""

    adult: SafetyLevel
    spoof: SafetyLevel
    medical: SafetyLevel
    violence: SafetyLevel
    racy: SafetyLevel


@dataclass
class ImageSafety:
    """Image safety analysis result."""

    safety_scores: SafetyScores
    is_safe: bool
    overall_risk: str


@dataclass
class ImageAnalysis:
    """Complete image analysis result."""

    labels: List[ImageLabel]
    description: str
    text: ImageText
    safety: ImageSafety
    image_path: str


class VisionRequest:
    """Base request model for vision operations."""

    def __init__(self, image_path: str):
        self.image_path = image_path

    def validate(self) -> bool:
        """Validate request parameters."""
        import os

        return os.path.exists(self.image_path)


class VisionResponse:
    """Base response model for vision operations."""

    def __init__(
        self, success: bool, data: Optional[Any] = None, error: Optional[str] = None
    ):
        self.success = success
        self.data = data
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        result = {"success": self.success}
        if self.data:
            result["data"] = self.data
        if self.error:
            result["error"] = self.error
        return result


def create_label_response(labels: List[Dict[str, Any]]) -> VisionResponse:
    """Create response for label detection."""
    if not labels:
        return VisionResponse(success=False, error="No labels detected")

    label_objects = [
        ImageLabel(
            description=label["description"], score=label["score"], mid=label["mid"]
        )
        for label in labels
    ]

    return VisionResponse(success=True, data=label_objects)


def create_text_response(text_data: Dict[str, Any]) -> VisionResponse:
    """Create response for text detection."""
    text_blocks = [
        TextDetection(text=block["text"], bounds=block["bounds"])
        for block in text_data.get("text_blocks", [])
    ]

    image_text = ImageText(
        full_text=text_data.get("full_text", ""), text_blocks=text_blocks
    )

    return VisionResponse(success=True, data=image_text)


def create_safety_response(safety_data: Dict[str, Any]) -> VisionResponse:
    """Create response for safety detection."""
    safety_scores = SafetyScores(
        adult=SafetyLevel(safety_data["safety_scores"]["adult"]),
        spoof=SafetyLevel(safety_data["safety_scores"]["spoof"]),
        medical=SafetyLevel(safety_data["safety_scores"]["medical"]),
        violence=SafetyLevel(safety_data["safety_scores"]["violence"]),
        racy=SafetyLevel(safety_data["safety_scores"]["racy"]),
    )

    image_safety = ImageSafety(
        safety_scores=safety_scores,
        is_safe=safety_data["is_safe"],
        overall_risk=safety_data["overall_risk"],
    )

    return VisionResponse(success=True, data=image_safety)
