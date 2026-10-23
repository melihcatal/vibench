from typing import Dict, Any, List


class ImagePayload:
    image_bytes: bytes


class LabelAnnotation:
    name: str
    confidence: float


class TextAnnotation:
    text: str
    confidence: float
    bounds: List[Dict[str, Any]]


class SafetyAnnotation:
    category: str
    likelihood: int  # Enum value, e.g., vision.Likelihood.LIKELY


class VisionApiResponse:
    labels: List[LabelAnnotation]
    text: str
    safety_scores: List[SafetyAnnotation]
    error: Dict[str, Any]
