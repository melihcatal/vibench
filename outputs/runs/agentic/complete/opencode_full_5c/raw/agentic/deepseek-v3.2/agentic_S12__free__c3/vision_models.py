from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SafetyLevel(Enum):
    SAFE = "safe"
    LOW_RISK = "low_risk"
    MEDIUM_RISK = "medium_risk"
    HIGH_RISK = "high_risk"


@dataclass
class ImageLabel:
    description: str
    confidence: float
    source: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ImageDescription:
    text: str
    language: str
    model: str
    confidence: Optional[float] = None


@dataclass
class DetectedText:
    text: str
    confidence: float
    bounding_box: Optional[Dict[str, float]] = None
    language: Optional[str] = None


@dataclass
class SafetyScore:
    adult_score: float
    racy_score: float
    gore_score: float
    overall_level: SafetyLevel

    @classmethod
    def from_scores(cls, adult: float, racy: float, gore: float) -> "SafetyScore":
        max_score = max(adult, racy, gore)
        if max_score < 0.3:
            level = SafetyLevel.SAFE
        elif max_score < 0.6:
            level = SafetyLevel.LOW_RISK
        elif max_score < 0.8:
            level = SafetyLevel.MEDIUM_RISK
        else:
            level = SafetyLevel.HIGH_RISK

        return cls(
            adult_score=adult, racy_score=racy, gore_score=gore, overall_level=level
        )


@dataclass
class ImageAnalysisResult:
    labels: List[ImageLabel]
    description: Optional[ImageDescription] = None
    detected_text: List[DetectedText] = None
    safety_score: Optional[SafetyScore] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "labels": [
                {
                    "description": label.description,
                    "confidence": label.confidence,
                    "source": label.source,
                    "metadata": label.metadata or {},
                }
                for label in self.labels
            ]
        }

        if self.description:
            result["description"] = {
                "text": self.description.text,
                "language": self.description.language,
                "model": self.description.model,
                "confidence": self.description.confidence,
            }

        if self.detected_text:
            result["detected_text"] = [
                {
                    "text": text.text,
                    "confidence": text.confidence,
                    "bounding_box": text.bounding_box,
                    "language": text.language,
                }
                for text in self.detected_text
            ]

        if self.safety_score:
            result["safety_score"] = {
                "adult_score": self.safety_score.adult_score,
                "racy_score": self.safety_score.racy_score,
                "gore_score": self.safety_score.gore_score,
                "overall_level": self.safety_score.overall_level.value,
            }

        return result


def normalize_google_vision_labels(
    labels_data: List[Dict[str, Any]],
) -> List[ImageLabel]:
    """
    Normalize Google Cloud Vision label data.

    Args:
        labels_data: Raw label data from Google Cloud Vision

    Returns:
        List of normalized ImageLabel objects
    """
    normalized = []
    for label in labels_data:
        normalized.append(
            ImageLabel(
                description=label.get("description", ""),
                confidence=label.get("score", 0.0),
                source="google-cloud-vision",
                metadata={
                    "topicality": label.get("topicality"),
                    "mid": label.get("mid"),
                },
            )
        )
    return normalized


def normalize_aws_rekognition_text(
    text_data: List[Dict[str, Any]],
) -> List[DetectedText]:
    """
    Normalize AWS Rekognition text detection data.

    Args:
        text_data: Raw text detection data from AWS Rekognition

    Returns:
        List of normalized DetectedText objects
    """
    normalized = []
    for text in text_data:
        normalized.append(
            DetectedText(
                text=text.get("text", ""),
                confidence=text.get("confidence", 0.0) / 100.0,
                bounding_box=text.get("geometry", {}).get("bounding_box"),
                language=None,
            )
        )
    return normalized


def normalize_azure_safety_score(safety_data: Dict[str, Any]) -> SafetyScore:
    """
    Normalize Azure Computer Vision safety score data.

    Args:
        safety_data: Raw safety data from Azure Computer Vision

    Returns:
        Normalized SafetyScore object
    """
    return SafetyScore.from_scores(
        adult=safety_data.get("adult_score", 0.0),
        racy=safety_data.get("racy_score", 0.0),
        gore=safety_data.get("gore_score", 0.0),
    )
