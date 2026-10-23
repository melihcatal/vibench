from typing import List, Dict, Optional
from pydantic import BaseModel


class ImageLabel(BaseModel):
    """Represents a label detected in an image."""

    description: str
    score: float
    topicality: Optional[float] = None


class ImageTextDetection(BaseModel):
    """Represents text detected in an image."""

    text: str
    bounding_box: List[Dict[str, float]]


class ImageDescription(BaseModel):
    """Represents a generated description for an image."""

    description: str
    confidence: Optional[float] = None


class ImageSafetyRating(BaseModel):
    """Represents a safety rating for an image."""

    category: str
    probability: str
    blocked: bool = False


def normalize_labels(labels: List[Dict]) -> List[ImageLabel]:
    """Normalize Google Cloud Vision label annotations into a standardized format."""
    return [
        ImageLabel(
            description=label.get("description", ""),
            score=label.get("score", 0.0),
            topicality=label.get("topicality", 0.0),
        )
        for label in labels
    ]


def normalize_text_detections(text_detections: List[Dict]) -> List[ImageTextDetection]:
    """Normalize Google Cloud Vision text detection annotations into a standardized format."""
    normalized = []
    for detection in text_detections:
        vertices = detection.get("bounding_box", {}).get("vertices", [])
        bounding_box = [
            {"x": vertex.get("x", 0.0), "y": vertex.get("y", 0.0)}
            for vertex in vertices
        ]
        normalized.append(
            ImageTextDetection(
                text=detection.get("description", ""), bounding_box=bounding_box
            )
        )
    return normalized


def normalize_safety_ratings(safety_ratings: List[Dict]) -> List[ImageSafetyRating]:
    """Normalize Google Cloud Vision safety ratings into a standardized format."""
    return [
        ImageSafetyRating(
            category=rating.get("category", ""),
            probability=rating.get("probability", "UNKNOWN"),
            blocked=rating.get("blocked", False),
        )
        for rating in safety_ratings
    ]
