
import dataclasses
from typing import List, Dict, Any, Optional

@dataclasses.dataclass
class ImageAnalysisRequest:
    image_url: str

@dataclasses.dataclass
class Label:
    name: str
    confidence: float

@dataclasses.dataclass
class ImageLabelResponse:
    labels: List[Label]

@dataclasses.dataclass
class TextDetection:
    text: str
    bounding_box: List[int]

@dataclasses.dataclass
class ImageTextResponse:
    detections: List[TextDetection]

@dataclasses.dataclass
class ImageDescriptionResponse:
    description: str

@dataclasses.dataclass
class SafetyScore:
    category: str
    score: float

@dataclasses.dataclass
class ImageSafetyResponse:
    safety_scores: List[SafetyScore]

