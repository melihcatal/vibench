from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ImageAnalysisRequest:
    image_path: str
    image_bytes: Optional[bytes] = None
    mime_type: str = "image/jpeg"


@dataclass
class NormalizedVisionResult:
    provider: str
    request_type: str
    items: List[Dict[str, Any]]
    raw: Dict[str, Any]


def normalize_aws_rekognition_labels(payload: Dict[str, Any]) -> NormalizedVisionResult:
    items = []
    for label in payload.get("Labels", []):
        items.append({"name": label.get("Name"), "confidence": label.get("Confidence")})
    return NormalizedVisionResult(provider="aws.rekognition", request_type="labels", items=items, raw=payload)


def normalize_aws_rekognition_text(payload: Dict[str, Any]) -> NormalizedVisionResult:
    items = []
    for det in payload.get("TextDetections", []):
        items.append({"text": det.get("DetectedText"), "confidence": det.get("Confidence"), "type": det.get("Type")})
    return NormalizedVisionResult(provider="aws.rekognition", request_type="text", items=items, raw=payload)


def normalize_aws_rekognition_moderation(payload: Dict[str, Any]) -> NormalizedVisionResult:
    items = []
    for det in payload.get("ModerationLabels", []):
        items.append({"name": det.get("Name"), "confidence": det.get("Confidence"), "parent": det.get("ParentName")})
    return NormalizedVisionResult(provider="aws.rekognition", request_type="safety", items=items, raw=payload)
