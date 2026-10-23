from typing import List, Dict, Optional, TypedDict
from pydantic import BaseModel


class Label(TypedDict):
    Name: str
    Confidence: float
    Parents: List[Dict[str, str]]


class TextDetection(TypedDict):
    DetectedText: str
    Confidence: float
    Type: str


class ModerationLabel(TypedDict):
    Name: str
    Confidence: float
    ParentName: str


class DetectLabelsResponse(BaseModel):
    Labels: List[Label]
    OrientationCorrection: Optional[str]


class DetectTextResponse(BaseModel):
    TextDetections: List[TextDetection]


class DetectModerationLabelsResponse(BaseModel):
    ModerationLabels: List[ModerationLabel]


def normalize_labels_response(response: Dict) -> DetectLabelsResponse:
    """Normalize AWS Rekognition labels response."""
    return DetectLabelsResponse(**response)


def normalize_text_detections(response: Dict) -> DetectTextResponse:
    """Normalize AWS Rekognition text detections response."""
    return DetectTextResponse(**response)


def normalize_moderation_labels(response: Dict) -> DetectModerationLabelsResponse:
    """Normalize AWS Rekognition moderation labels response."""
    return DetectModerationLabelsResponse(**response)


def extract_text_detections(text_detections: List[TextDetection]) -> List[str]:
    """Extract detected text from text detections."""
    return [
        detection["DetectedText"]
        for detection in text_detections
        if detection["Type"] == "LINE"
    ]
