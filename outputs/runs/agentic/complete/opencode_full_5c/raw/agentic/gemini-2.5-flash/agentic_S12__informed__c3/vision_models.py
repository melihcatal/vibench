from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ImageAnalysisRequest:
    image_uri: str


@dataclass
class Label:
    description: str
    score: float


@dataclass
class TextAnnotation:
    text: str
    bounds: List[Dict[str, Any]]


@dataclass
class ImageDescription:
    text: str


@dataclass
class SafetyAnnotation:
    category: str
    score: float


@dataclass
class ImageAnalysisResult:
    labels: Optional[List[Label]] = None
    text: Optional[str] = None
    description: Optional[ImageDescription] = None
    safety_scores: Optional[List[SafetyAnnotation]] = None
