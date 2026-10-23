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
    """Represents a detected label in an image."""

    description: str
    score: float
    mid: Optional[str] = None
    topicality: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "description": self.description,
            "score": self.score,
            "mid": self.mid,
            "topicality": self.topicality,
        }


@dataclass
class DetectedText:
    """Represents detected text in an image."""

    text: str
    confidence: float
    bounding_box: Optional[List[tuple]] = None
    text_type: str = "text_block"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "text": self.text,
            "confidence": self.confidence,
            "bounding_box": self.bounding_box,
            "type": self.text_type,
        }


@dataclass
class ImageDescription:
    """Represents an image description."""

    description: str
    confidence: float
    provider: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "description": self.description,
            "confidence": self.confidence,
            "provider": self.provider,
        }


@dataclass
class SafetyScores:
    """Represents safety scores for an image."""

    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "adult": self.adult,
            "spoof": self.spoof,
            "medical": self.medical,
            "violence": self.violence,
            "racy": self.racy,
        }


@dataclass
class SafetyResult:
    """Represents safety analysis result."""

    is_safe: bool
    safety_scores: SafetyScores
    provider: str
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "is_safe": self.is_safe,
            "safety_scores": self.safety_scores.to_dict(),
            "provider": self.provider,
            "recommendation": self.recommendation,
        }


def normalize_labels(labels_data: List[Dict[str, Any]]) -> List[ImageLabel]:
    """Normalize label data from API response."""
    normalized = []
    for label in labels_data:
        normalized.append(
            ImageLabel(
                description=label.get("description", ""),
                score=label.get("score", 0.0),
                mid=label.get("mid"),
                topicality=label.get("topicality"),
            )
        )
    return normalized


def normalize_text_detection(text_data: List[Dict[str, Any]]) -> List[DetectedText]:
    """Normalize text detection data from API response."""
    normalized = []
    for text in text_data:
        normalized.append(
            DetectedText(
                text=text.get("text", ""),
                confidence=text.get("confidence", 0.0),
                bounding_box=text.get("bounding_box"),
                text_type=text.get("type", "text_block"),
            )
        )
    return normalized
