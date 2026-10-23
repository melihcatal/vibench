from typing import List, Dict, Any

class ImageAnalysisRequest:
    image_bytes: bytes

    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes


class LabelResult:
    name: str
    confidence: float

    def __init__(self, name: str, confidence: float):
        self.name = name
        self.confidence = confidence


class DescriptionResult:
    text: str
    confidence: float

    def __init__(self, text: str, confidence: float):
        self.text = text
        self.confidence = confidence


class TextResult:
    text: str
    bounding_polygon: List[Dict[str, float]]

    def __init__(self, text: str, bounding_polygon: List[Dict[str, float]]):
        self.text = text
        self.bounding_polygon = bounding_polygon


class SafetyResult:
    category: str
    severity: int

    def __init__(self, category: str, severity: int):
        self.category = category
        self.severity = severity
