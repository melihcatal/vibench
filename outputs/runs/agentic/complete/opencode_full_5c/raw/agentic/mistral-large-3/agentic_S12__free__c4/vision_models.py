from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ImageLabel:
    """Represents a detected label in an image."""

    description: str
    score: float


@dataclass
class ImageText:
    """Represents detected text in an image."""

    description: str
    bounding_poly: Optional[List[Dict[str, int]]] = None


@dataclass
class ImageSafety:
    """Represents safety ratings for an image."""

    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str


@dataclass
class ImageDescription:
    """Represents a visual description of an image."""

    colors: List[str]
    labels: List[str]
    description: str


class VisionModels:
    """Local request, response and normalization helpers for Google Cloud Vision API."""

    @staticmethod
    def normalize_labels(labels: List[Dict[str, Any]]) -> List[ImageLabel]:
        """Normalizes label detection results."""
        return [
            ImageLabel(description=label.description, score=label.score)
            for label in labels
        ]

    @staticmethod
    def normalize_text(texts: List[Dict[str, Any]]) -> List[ImageText]:
        """Normalizes text detection results."""
        return [
            ImageText(
                description=text.description,
                bounding_poly=text.bounding_poly.vertices
                if hasattr(text, "bounding_poly")
                else None,
            )
            for text in texts
        ]

    @staticmethod
    def normalize_safety(safety: Dict[str, str]) -> ImageSafety:
        """Normalizes safety detection results."""
        return ImageSafety(
            adult=safety.get("adult", "UNKNOWN"),
            spoof=safety.get("spoof", "UNKNOWN"),
            medical=safety.get("medical", "UNKNOWN"),
            violence=safety.get("violence", "UNKNOWN"),
            racy=safety.get("racy", "UNKNOWN"),
        )

    @staticmethod
    def normalize_description(description: Dict[str, Any]) -> ImageDescription:
        """Normalizes image description results."""
        return ImageDescription(
            colors=description.get("colors", []),
            labels=description.get("labels", []),
            description=description.get("description", ""),
        )
