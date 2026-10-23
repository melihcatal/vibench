from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SafetyLevel(Enum):
    """Safety level enumeration."""

    VERY_UNLIKELY = "VERY_UNLIKELY"
    UNLIKELY = "UNLIKELY"
    POSSIBLE = "POSSIBLE"
    LIKELY = "LIKELY"
    VERY_LIKELY = "VERY_LIKELY"


@dataclass
class LabelResult:
    """Normalized label detection result."""

    description: str
    score: float
    topicality: Optional[float] = None
    mid: Optional[str] = None

    @classmethod
    def from_google_vision(cls, label) -> "LabelResult":
        """Create from Google Cloud Vision label annotation."""
        return cls(
            description=label.description,
            score=label.score,
            topicality=getattr(label, "topicality", None),
            mid=getattr(label, "mid", None),
        )


@dataclass
class TextDetectionResult:
    """Normalized text detection result."""

    text: str
    confidence: Optional[float] = None
    bounding_box: Optional[List[tuple]] = None

    @classmethod
    def from_google_vision(cls, text_annotation) -> "TextDetectionResult":
        """Create from Google Cloud Vision text annotation."""
        bounding_box = None
        if (
            hasattr(text_annotation, "bounding_poly")
            and text_annotation.bounding_poly.vertices
        ):
            bounding_box = [
                (vertex.x, vertex.y)
                for vertex in text_annotation.bounding_poly.vertices
            ]

        return cls(
            text=text_annotation.description,
            confidence=getattr(text_annotation, "confidence", None),
            bounding_box=bounding_box,
        )


@dataclass
class SafetyResult:
    """Normalized safety detection result."""

    adult: SafetyLevel
    violence: SafetyLevel
    racy: SafetyLevel
    medical: SafetyLevel
    spoof: SafetyLevel

    @property
    def is_safe(self) -> bool:
        """Check if image is considered safe."""
        unsafe_levels = {SafetyLevel.LIKELY, SafetyLevel.VERY_LIKELY}
        return all(
            getattr(self, category) not in unsafe_levels
            for category in ["adult", "violence", "racy"]
        )

    @classmethod
    def from_google_vision(cls, safe_search) -> "SafetyResult":
        """Create from Google Cloud Vision safe search annotation."""
        return cls(
            adult=SafetyLevel(safe_search.adult.name),
            violence=SafetyLevel(safe_search.violence.name),
            racy=SafetyLevel(safe_search.racy.name),
            medical=SafetyLevel(safe_search.medical.name),
            spoof=SafetyLevel(safe_search.spoof.name),
        )


@dataclass
class ImageDescription:
    """Normalized image description result."""

    summary: str
    labels: List[str]
    confidence_scores: List[float]

    @classmethod
    def from_labels(
        cls, labels: List[LabelResult], top_n: int = 5
    ) -> "ImageDescription":
        """Create from list of labels."""
        top_labels = sorted(labels, key=lambda x: x.score, reverse=True)[:top_n]
        summary = "This image contains: " + ", ".join(
            [label.description for label in top_labels]
        )

        return cls(
            summary=summary,
            labels=[label.description for label in labels],
            confidence_scores=[label.score for label in labels],
        )


def normalize_label_response(labels: List[Any]) -> List[Dict[str, Any]]:
    """Normalize label response to consistent format."""
    return [
        {
            "description": label.description,
            "score": label.score,
            "topicality": getattr(label, "topicality", None),
            "mid": getattr(label, "mid", None),
        }
        for label in labels
    ]


def normalize_text_response(texts: List[Any]) -> List[Dict[str, Any]]:
    """Normalize text detection response to consistent format."""
    if not texts:
        return []

    result = []
    for text in texts[1:]:  # Skip first element containing all text
        bounding_box = None
        if hasattr(text, "bounding_poly") and text.bounding_poly.vertices:
            bounding_box = [
                (vertex.x, vertex.y) for vertex in text.bounding_poly.vertices
            ]

        result.append(
            {
                "text": text.description,
                "confidence": getattr(text, "confidence", None),
                "bounding_box": bounding_box,
            }
        )

    return result
