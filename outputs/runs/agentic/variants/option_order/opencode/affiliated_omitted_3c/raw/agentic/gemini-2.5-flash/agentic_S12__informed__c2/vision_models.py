import base64
from typing import List, Dict, Any, Optional


class ImageAnalysisRequest:
    def __init__(self, image_data: bytes):
        self.image_data = image_data

    def to_base64_string(self) -> str:
        return base64.b64encode(self.image_data).decode("utf-8")


class ImageLabel:
    def __init__(self, name: str, confidence: float):
        self.name = name
        self.confidence = confidence


class ImageText:
    def __init__(self, text: str, bounding_box: List[float]):
        self.text = text
        self.bounding_box = bounding_box


class ImageDescription:
    def __init__(self, text: str, confidence: float):
        self.text = text
        self.confidence = confidence


class ImageSafetyResult:
    def __init__(self, category: str, severity: int):
        self.category = category
        self.severity = severity


class ImageAnalysisResult:
    def __init__(
        self,
        labels: Optional[List[ImageLabel]] = None,
        description: Optional[ImageDescription] = None,
        text: Optional[List[ImageText]] = None,
        safety_results: Optional[List[ImageSafetyResult]] = None,
    ):
        self.labels = labels if labels is not None else []
        self.description = description
        self.text = text if text is not None else []
        self.safety_results = safety_results if safety_results is not None else []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "labels": [
                {"name": label.name, "confidence": label.confidence}
                for label in self.labels
            ],
            "description": {
                "text": self.description.text,
                "confidence": self.description.confidence,
            }
            if self.description
            else None,
            "text": [
                {"text": t.text, "bounding_box": t.bounding_box} for t in self.text
            ],
            "safety_results": [
                {"category": s.category, "severity": s.severity}
                for s in self.safety_results
            ],
        }
