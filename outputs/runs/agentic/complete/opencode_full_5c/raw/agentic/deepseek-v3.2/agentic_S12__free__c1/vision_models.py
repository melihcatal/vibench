from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SafetyCategory(str, Enum):
    VIOLENCE = "violence"
    HATE = "hate"
    SEXUAL = "sexual"
    HARASSMENT = "harassment"
    SELF_HARM = "self_harm"
    GRAPHIC = "graphic"


@dataclass
class ImageLabel:
    description: str
    score: float
    topicality: Optional[float] = None
    mid: Optional[str] = None


@dataclass
class TextDetection:
    text: str
    confidence: float
    geometry: Dict[str, Any]


@dataclass
class SafetyScore:
    flagged: bool
    categories: Dict[SafetyCategory, bool]
    category_scores: Dict[SafetyCategory, float]


@dataclass
class ImageAnalysisResult:
    labels: List[ImageLabel]
    description: Optional[str] = None
    text_detections: List[TextDetection] = None
    safety_score: Optional[SafetyScore] = None

    def __post_init__(self):
        if self.text_detections is None:
            self.text_detections = []


@dataclass
class TranslationRequest:
    text: str
    source_language: str = "auto"
    target_language: str = "en"


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class ArchiveMetadata:
    image_path: str
    analysis_results: Dict[str, Any]
    timestamp: str
    bucket_name: str
    object_key: str


def normalize_labels(labels_data: List[Dict[str, Any]]) -> List[ImageLabel]:
    """Normalize label data from different providers."""
    normalized = []
    for label in labels_data:
        normalized.append(
            ImageLabel(
                description=label.get("description", ""),
                score=float(label.get("score", 0.0)),
                topicality=label.get("topicality"),
                mid=label.get("mid"),
            )
        )
    return normalized


def normalize_text_detections(
    detections_data: List[Dict[str, Any]],
) -> List[TextDetection]:
    """Normalize text detection data from different providers."""
    normalized = []
    for detection in detections_data:
        normalized.append(
            TextDetection(
                text=detection.get("text", ""),
                confidence=float(detection.get("confidence", 0.0)),
                geometry=detection.get("geometry", {}),
            )
        )
    return normalized


def normalize_safety_score(safety_data: Dict[str, Any]) -> SafetyScore:
    """Normalize safety score data from different providers."""
    categories = {}
    category_scores = {}

    for category_name, flagged in safety_data.get("categories", {}).items():
        try:
            category = SafetyCategory(category_name)
            categories[category] = bool(flagged)
            category_scores[category] = float(
                safety_data.get("category_scores", {}).get(category_name, 0.0)
            )
        except ValueError:
            continue

    return SafetyScore(
        flagged=bool(safety_data.get("flagged", False)),
        categories=categories,
        category_scores=category_scores,
    )
