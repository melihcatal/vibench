from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ImageAnalysisPayload:
    image_bytes: bytes

@dataclass
class Label:
    name: str
    confidence: float

@dataclass
class LabelsResponse:
    labels: List[Label]

@dataclass
class DescriptionResponse:
    description: str
    confidence: float

@dataclass
class TextDetectionResponse:
    text_content: str

@dataclass
class SafetyScore:
    is_adult_content: bool
    is_racy_content: bool
    is_gory_content: bool
    adult_score: float
    racy_score: float
    gory_score: float

@dataclass
class ViolenceScore:
    has_violence: bool
    violence_score: float

@dataclass
class SafetyResponse:
    adult: SafetyScore
    violence: ViolenceScore
