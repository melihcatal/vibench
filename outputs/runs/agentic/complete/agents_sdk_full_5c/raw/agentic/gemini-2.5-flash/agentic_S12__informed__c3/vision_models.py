
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ImageAnalysisRequest:
    image_uri: Optional[str] = None
    image_data: Optional[bytes] = None

@dataclass
class LabelDetectionResult:
    labels: List[str]

@dataclass
class ImageDescriptionResult:
    description: str

@dataclass
class TextDetectionResult:
    text: str

@dataclass
class SafetyScoreResult:
    scores: Dict[str, str]

@dataclass
class ImageAnalysisReport:
    image_uri: str
    labels: Optional[List[str]] = None
    description: Optional[str] = None
    detected_text: Optional[str] = None
    safety_scores: Optional[Dict[str, str]] = None
