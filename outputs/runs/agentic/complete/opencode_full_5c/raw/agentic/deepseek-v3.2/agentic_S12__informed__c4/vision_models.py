from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ImageAnalysisType(Enum):
    LABELS = "labels"
    TEXT = "text"
    DESCRIPTION = "description"
    SAFETY = "safety"


@dataclass
class ImageLabel:
    name: str
    confidence: float
    parents: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"name": self.name, "confidence": self.confidence}
        if self.parents:
            result["parents"] = self.parents
        return result


@dataclass
class TextDetection:
    text: str
    confidence: float
    type: str

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "confidence": self.confidence, "type": self.type}


@dataclass
class ImageDescription:
    description: str
    labels: List[str]
    confidence: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "labels": self.labels,
            "confidence": self.confidence,
        }


@dataclass
class SafetyScore:
    is_safe: bool
    moderation_labels: List[Dict[str, Any]]
    safety_score: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "moderation_labels": self.moderation_labels,
            "safety_score": self.safety_score,
        }


def normalize_labels(rekognition_labels: List[Dict[str, Any]]) -> List[ImageLabel]:
    """Normalize Amazon Rekognition labels to ImageLabel objects."""
    labels = []
    for label in rekognition_labels:
        parents = [parent["Name"] for parent in label.get("Parents", [])]
        labels.append(
            ImageLabel(
                name=label["Name"],
                confidence=label["Confidence"],
                parents=parents if parents else None,
            )
        )
    return labels


def normalize_text_detections(
    rekognition_detections: List[Dict[str, Any]],
) -> List[TextDetection]:
    """Normalize Amazon Rekognition text detections to TextDetection objects."""
    detections = []
    for detection in rekognition_detections:
        detections.append(
            TextDetection(
                text=detection["DetectedText"],
                confidence=detection["Confidence"],
                type=detection["Type"],
            )
        )
    return detections
