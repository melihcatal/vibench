from typing import TypedDict, List, Dict, Any

class ImageLabels(TypedDict):
    labels: List[Dict[str, Any]]

class ImageCaption(TypedDict):
    caption: str
    confidence: float

class ImageTextAnnotation(TypedDict):
    full_text: str
    detections: List[Dict[str, Any]]

class ImageSafetyReport(TypedDict):
    is_safe: bool
    risks: List[str]