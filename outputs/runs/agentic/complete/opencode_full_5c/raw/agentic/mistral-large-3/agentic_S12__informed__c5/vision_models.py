from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Label:
    """Represents a detected label in an image."""

    name: str
    confidence: float

    def to_dict(self) -> Dict[str, float]:
        return {"Label": self.name, "Confidence": self.confidence}


@dataclass
class TextRegion:
    """Represents a detected text region in an image."""

    text: str
    bounding_box: List[float]

    def to_dict(self) -> Dict[str, str]:
        return {"text": self.text, "bounding_box": str(self.bounding_box)}


@dataclass
class ImageDescription:
    """Represents a visual description of an image."""

    description: str
    labels: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {"description": self.description, "labels": self.labels}


@dataclass
class SafetyScore:
    """Represents unsafe content detected in an image."""

    category: str
    concepts: List[Dict[str, float]]

    def to_dict(self) -> Dict[str, Any]:
        return {self.category: self.concepts}


def normalize_labels(labels: List[Dict[str, Any]]) -> List[Dict[str, float]]:
    """Normalizes label detection results."""
    return [
        {"Label": label["Name"], "Confidence": label["Confidence"]} for label in labels
    ]


def normalize_text_regions(text_regions: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Normalizes text detection results."""
    return [
        {"text": region["text"], "bounding_box": str(region["boundingBox"])}
        for region in text_regions
    ]


def normalize_safety_scores(
    safety_scores: Dict[str, List[Dict[str, float]]],
) -> Dict[str, List[Dict[str, float]]]:
    """Normalizes safety scoring results."""
    return safety_scores
