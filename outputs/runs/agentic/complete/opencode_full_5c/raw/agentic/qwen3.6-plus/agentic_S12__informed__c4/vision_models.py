import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ImageAnalysisRequest:
    image_url: Optional[str] = None
    image_bytes: Optional[bytes] = None
    image_format: str = "jpeg"


@dataclass
class DetectedLabel:
    name: str
    confidence: float
    parent_labels: List[str] = field(default_factory=list)


@dataclass
class LabelDetectionResponse:
    labels: List[DetectedLabel]
    image_width: int = 0
    image_height: int = 0
    model: str = "amazon-rekognition"


@dataclass
class ImageDescriptionResponse:
    description: str
    tags: List[str] = field(default_factory=list)
    confidence: float = 0.0
    model: str = "amazon-rekognition"


@dataclass
class DetectedText:
    text: str
    confidence: float
    bounding_box: Optional[dict] = None


@dataclass
class TextDetectionResponse:
    detected_texts: List[DetectedText]
    full_text: str = ""
    model: str = "amazon-rekognition"


@dataclass
class SafetyCategory:
    name: str
    confidence: float
    parent_name: Optional[str] = None


@dataclass
class SafetyScoreResponse:
    is_safe: bool
    categories: List[SafetyCategory]
    threshold: float = 0.5
    model: str = "amazon-rekognition"


@dataclass
class ImageSummaryRequest:
    labels: List[DetectedLabel]
    description: str
    detected_texts: List[str]
    safety_result: Optional[SafetyScoreResponse] = None


@dataclass
class ImageSummaryResponse:
    summary: str
    model: str = "anthropic-claude"


@dataclass
class TranslationRequest:
    text: str
    source_language: str = "en"
    target_language: str = "es"


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    model: str = "google-translate"


@dataclass
class TextSafetyRequest:
    text: str
    categories: List[str] = field(
        default_factory=lambda: ["HATE", "SELF_HARM", "SEXUAL", "VIOLENCE"]
    )


@dataclass
class TextSafetyScore:
    category: str
    score: float


@dataclass
class TextSafetyResponse:
    is_safe: bool
    scores: List[TextSafetyScore]
    model: str = "azure-content-safety"


@dataclass
class ArchiveRequest:
    bucket_name: str
    prefix: str
    artifacts: dict


@dataclass
class ArchiveResponse:
    archived_keys: List[str]
    bucket: str
    model: str = "amazon-s3"


def normalize_labels(
    raw_labels: list, confidence_threshold: float = 0.0
) -> List[DetectedLabel]:
    labels = []
    for item in raw_labels:
        conf = item.get("Confidence", 0.0)
        if conf >= confidence_threshold:
            parents = [p.get("Name", "") for p in item.get("Parents", [])]
            labels.append(
                DetectedLabel(
                    name=item.get("Name", "unknown"),
                    confidence=conf,
                    parent_labels=parents,
                )
            )
    return labels


def normalize_moderation(
    raw_labels: list, threshold: float = 0.5
) -> SafetyScoreResponse:
    categories = []
    has_violation = False
    for item in raw_labels:
        conf = item.get("Confidence", 0.0)
        cat = SafetyCategory(
            name=item.get("Name", "unknown"),
            confidence=conf,
            parent_name=item.get("ParentName"),
        )
        categories.append(cat)
        if conf >= threshold * 100:
            has_violation = True
    return SafetyScoreResponse(
        is_safe=not has_violation, categories=categories, threshold=threshold
    )


def normalize_text_detections(
    raw_detections: list, confidence_threshold: float = 0.0
) -> List[DetectedText]:
    texts = []
    for item in raw_detections:
        if item.get("Type") == "LINE":
            conf = item.get("Confidence", 0.0)
            if conf >= confidence_threshold:
                bbox = item.get("Geometry", {}).get("BoundingBox", {})
                texts.append(
                    DetectedText(
                        text=item.get("DetectedText", ""),
                        confidence=conf,
                        bounding_box=bbox,
                    )
                )
    return texts
