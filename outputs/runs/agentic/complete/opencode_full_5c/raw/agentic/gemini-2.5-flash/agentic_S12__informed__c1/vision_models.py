from typing import List, Optional, Dict, Any


class ImageRequest:
    def __init__(self, image_uri: str):
        self.image_uri = image_uri


class LabelDetectionResponse:
    def __init__(self, labels: List[str]):
        self.labels = labels


class DescriptionResponse:
    def __init__(self, description: str):
        self.description = description


class TextDetectionResponse:
    def __init__(self, text_annotations: List[Dict[str, Any]]):
        self.text_annotations = text_annotations


class SafetyDetectionResponse:
    def __init__(self, safety_annotations: Dict[str, str]):
        self.safety_annotations = safety_annotations


class ImageAnalysisResult:
    def __init__(
        self,
        image_uri: str,
        labels: Optional[List[str]] = None,
        description: Optional[str] = None,
        text_annotations: Optional[List[Dict[str, Any]]] = None,
        safety_annotations: Optional[Dict[str, str]] = None,
    ):
        self.image_uri = image_uri
        self.labels = labels
        self.description = description
        self.text_annotations = text_annotations
        self.safety_annotations = safety_annotations
