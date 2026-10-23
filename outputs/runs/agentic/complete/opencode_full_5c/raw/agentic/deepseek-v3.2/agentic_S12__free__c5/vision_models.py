from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "Hate"
    SELF_HARM = "SelfHarm"
    SEXUAL = "Sexual"
    VIOLENCE = "Violence"


@dataclass
class LabelDetection:
    description: str
    score: float
    source: str = "google"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "score": self.score,
            "source": self.source,
        }


@dataclass
class TextDetection:
    text: str
    confidence: float
    bounding_box: Optional[Dict[str, float]] = None
    source: str = "aws"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "bounding_box": self.bounding_box,
            "source": self.source,
        }


@dataclass
class ImageDescription:
    description: str
    source: str = "openai"

    def to_dict(self) -> Dict[str, Any]:
        return {"description": self.description, "source": self.source}


@dataclass
class SafetyScore:
    category: SafetyCategory
    severity: int
    confidence: float
    source: str = "azure"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category.value,
            "severity": self.severity,
            "confidence": self.confidence,
            "source": self.source,
        }


@dataclass
class ImageAnalysisResult:
    labels: List[LabelDetection]
    text_detections: List[TextDetection]
    description: Optional[ImageDescription] = None
    safety_scores: Optional[List[SafetyScore]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "labels": [label.to_dict() for label in self.labels],
            "text_detections": [text.to_dict() for text in self.text_detections],
        }

        if self.description:
            result["description"] = self.description.to_dict()

        if self.safety_scores:
            result["safety_scores"] = [score.to_dict() for score in self.safety_scores]

        return result


def normalize_google_labels(google_labels: List[Dict]) -> List[LabelDetection]:
    """Normalize Google Cloud Vision label detection results."""
    return [
        LabelDetection(
            description=label["description"], score=label["score"], source="google"
        )
        for label in google_labels
    ]


def normalize_aws_text_detections(aws_detections: List[Dict]) -> List[TextDetection]:
    """Normalize AWS Rekognition text detection results."""
    return [
        TextDetection(
            text=detection["text"],
            confidence=detection["confidence"] / 100.0,  # Normalize to 0-1
            bounding_box=detection.get("bounding_box"),
            source="aws",
        )
        for detection in aws_detections
    ]


def normalize_openai_description(description: str) -> ImageDescription:
    """Normalize OpenAI Vision API description result."""
    return ImageDescription(description=description.strip(), source="openai")


def normalize_azure_safety_scores(azure_result: Dict[str, Any]) -> List[SafetyScore]:
    """Normalize Azure Content Safety results."""
    safety_scores = []

    for category_name, score_data in azure_result.get("safety_scores", {}).items():
        try:
            category = SafetyCategory(category_name)
            safety_scores.append(
                SafetyScore(
                    category=category,
                    severity=score_data.get("severity", 0),
                    confidence=score_data.get("score", 0) / 10.0,  # Normalize to 0-1
                    source="azure",
                )
            )
        except ValueError:
            continue

    return safety_scores
