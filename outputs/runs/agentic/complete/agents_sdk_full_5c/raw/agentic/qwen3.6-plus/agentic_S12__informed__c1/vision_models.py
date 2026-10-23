"""
vision_models.py - Local request, response, and normalization helpers
for Static Image and Visual Understanding via Amazon Rekognition.

Provider: Amazon Rekognition
SDK: boto3
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ImageLabel:
    """Represents a detected label from Amazon Rekognition."""
    name: str
    confidence: float
    parent_labels: List[str] = field(default_factory=list)
    instances: List[Dict[str, float]] = field(default_factory=list)

    @classmethod
    def from_rekognition_response(cls, label_dict: Dict[str, Any]) -> "ImageLabel":
        """Normalize a Rekognition label response dict into an ImageLabel."""
        return cls(
            name=label_dict.get("Name", ""),
            confidence=label_dict.get("Confidence", 0.0),
            parent_labels=[
                p.get("Name", "") for p in label_dict.get("Parents", [])
            ],
            instances=[
                {
                    "confidence": inst.get("Confidence", 0.0),
                    "bounding_box": inst.get("BoundingBox", {}),
                }
                for inst in label_dict.get("Instances", [])
            ],
        )


@dataclass
class DetectedTextRegion:
    """Represents a text region detected in an image by Amazon Rekognition."""
    detected_text: str
    confidence: float
    label_type: str  # "WORD" or "LINE"
    bounding_box: Dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_rekognition_response(cls, text_detection: Dict[str, Any]) -> "DetectedTextRegion":
        """Normalize a Rekognition text detection dict."""
        return cls(
            detected_text=text_detection.get("DetectedText", ""),
            confidence=text_detection.get("Confidence", 0.0),
            label_type=text_detection.get("Type", "WORD"),
            bounding_box=text_detection.get("Geometry", {}).get("BoundingBox", {}),
        )


@dataclass
class SafetyFinding:
    """Represents a safety or moderation finding from Amazon Rekognition."""
    label_type: str
    name: str
    confidence: float
    parent_name: Optional[str] = None

    @classmethod
    def from_rekognition_response(cls, moderation: Dict[str, Any]) -> "SafetyFinding":
        """Normalize a Rekognition moderation label response."""
        parent_list = moderation.get("ParentName", [])
        return cls(
            label_type=moderation.get("Name", ""),
            name=moderation.get("Name", ""),
            confidence=moderation.get("Confidence", 0.0),
            parent_name=parent_list if isinstance(parent_list, str) else None,
        )


@dataclass
class ImageLabelResult:
    """Aggregated result from label detection."""
    labels: List[ImageLabel]
    label_model_version: str
    orientation_correction: Optional[str] = None

    @classmethod
    def from_rekognition_response(cls, response: Dict[str, Any]) -> "ImageLabelResult":
        labels = [
            ImageLabel.from_rekognition_response(lbl)
            for lbl in response.get("Labels", [])
        ]
        return cls(
            labels=labels,
            label_model_version=response.get("LabelModelVersion", ""),
            orientation_correction=response.get("OrientationCorrection"),
        )


@dataclass
class ImageTextResult:
    """Aggregated result from text detection in images."""
    text_detections: List[DetectedTextRegion]
    text_model_version: str

    @classmethod
    def from_rekognition_response(cls, response: Dict[str, Any]) -> "ImageTextResult":
        detections = [
            DetectedTextRegion.from_rekognition_response(td)
            for td in response.get("TextDetections", [])
        ]
        return cls(
            text_detections=detections,
            text_model_version=response.get("TextModelVersion", ""),
        )


@dataclass
class ImageSafetyResult:
    """Aggregated result from content moderation."""
    moderation_labels: List[SafetyFinding]
    moderation_model_version: str
    human_loop_activation_output: Optional[str] = None

    @classmethod
    def from_rekognition_response(cls, response: Dict[str, Any]) -> "ImageSafetyResult":
        labels = [
            SafetyFinding.from_rekognition_response(mod)
            for mod in response.get("ModerationLabels", [])
        ]
        return cls(
            moderation_labels=labels,
            moderation_model_version=response.get("ModerationModelVersion", ""),
            human_loop_activation_output=response.get("HumanLoopActivationOutput"),
        )


def normalize_label_list_for_summary(
    labels: List[ImageLabel],
    min_confidence: float = 50.0,
    max_labels: int = 15,
) -> List[Dict[str, Any]]:
    """Filter and truncate labels for downstream summarization."""
    filtered = [
        {"name": lbl.name, "confidence": round(lbl.confidence, 2)}
        for lbl in labels
        if lbl.confidence >= min_confidence
    ]
    return filtered[:max_labels]


def extract_detected_text_lines(
    text_result: ImageTextResult,
    min_confidence: float = 70.0,
) -> str:
    """Extract readable lines from text detection results."""
    lines = [
        td.detected_text
        for td in text_result.text_detections
        if td.label_type == "LINE" and td.confidence >= min_confidence
    ]
    return " ".join(lines)


def compute_safety_score(safety_result: ImageSafetyResult) -> float:
    """
    Compute a safety score from 0.0 (unsafe) to 1.0 (safe).
    Higher confidence moderation labels reduce the score.
    """
    if not safety_result.moderation_labels:
        return 1.0

    max_confidence = max(
        lbl.confidence for lbl in safety_result.moderation_labels
    )
    return round(max(0.0, 1.0 - (max_confidence / 100.0)), 3)
