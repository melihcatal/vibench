from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SafetyLevel(Enum):
    UNKNOWN = "UNKNOWN"
    VERY_UNLIKELY = "VERY_UNLIKELY"
    UNLIKELY = "UNLIKELY"
    POSSIBLE = "POSSIBLE"
    LIKELY = "LIKELY"
    VERY_LIKELY = "VERY_LIKELY"


@dataclass
class ImageLabel:
    description: str
    confidence: float
    topicality: Optional[float] = None

    @classmethod
    def from_google_vision(cls, label_annotation):
        return cls(
            description=label_annotation.description,
            confidence=label_annotation.score,
            topicality=label_annotation.topicality
            if hasattr(label_annotation, "topicality")
            else None,
        )

    @classmethod
    def from_aws_rekognition(cls, label_data):
        return cls(
            description=label_data["Name"],
            confidence=label_data["Confidence"] / 100.0,
            topicality=None,
        )


@dataclass
class DetectedText:
    text: str
    bounding_box: Optional[List[tuple]] = None

    @classmethod
    def from_google_vision(cls, text_annotation):
        bounding_box = []
        if hasattr(text_annotation, "bounding_poly"):
            for vertex in text_annotation.bounding_poly.vertices:
                bounding_box.append((vertex.x, vertex.y))

        return cls(
            text=text_annotation.description,
            bounding_box=bounding_box if bounding_box else None,
        )


@dataclass
class SafetyScores:
    adult: SafetyLevel
    spoof: SafetyLevel
    medical: SafetyLevel
    violence: SafetyLevel
    racy: SafetyLevel

    @classmethod
    def from_google_vision(cls, safe_search_annotation):
        return cls(
            adult=SafetyLevel(safe_search_annotation.adult.name),
            spoof=SafetyLevel(safe_search_annotation.spoof.name),
            medical=SafetyLevel(safe_search_annotation.medical.name),
            violence=SafetyLevel(safe_search_annotation.violence.name),
            racy=SafetyLevel(safe_search_annotation.racy.name),
        )

    def is_safe(self) -> bool:
        unsafe_levels = {SafetyLevel.LIKELY, SafetyLevel.VERY_LIKELY}
        return all(
            [
                self.adult not in unsafe_levels,
                self.spoof not in unsafe_levels,
                self.medical not in unsafe_levels,
                self.violence not in unsafe_levels,
                self.racy not in unsafe_levels,
            ]
        )


@dataclass
class ImageAnalysisResult:
    labels: List[ImageLabel]
    description: Optional[str] = None
    detected_text: Optional[DetectedText] = None
    safety_scores: Optional[SafetyScores] = None
    image_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "labels": [
                {"description": label.description, "confidence": label.confidence}
                for label in self.labels
            ],
            "has_description": self.description is not None,
            "has_detected_text": self.detected_text is not None,
            "has_safety_scores": self.safety_scores is not None,
            "image_path": self.image_path,
        }

        if self.description:
            result["description"] = self.description

        if self.detected_text:
            result["detected_text"] = {
                "text": self.detected_text.text,
                "has_bounding_box": self.detected_text.bounding_box is not None,
            }

        if self.safety_scores:
            result["safety_scores"] = {
                "adult": self.safety_scores.adult.value,
                "spoof": self.safety_scores.spoof.value,
                "medical": self.safety_scores.medical.value,
                "violence": self.safety_scores.violence.value,
                "racy": self.safety_scores.racy.value,
                "is_safe": self.safety_scores.is_safe(),
            }

        return result
