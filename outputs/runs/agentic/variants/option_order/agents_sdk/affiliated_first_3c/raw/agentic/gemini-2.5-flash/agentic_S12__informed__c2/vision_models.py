from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ImageAnalysisRequest:
    image_uri: str

@dataclass
class LabelDetectionResult:
    description: str
    score: float

@dataclass
class TextDetectionResult:
    text: str

@dataclass
class SafeSearchResult:
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str

@dataclass
class ImageAnalysisResponse:
    image_uri: str
    labels: Optional[List[LabelDetectionResult]] = None
    description: Optional[str] = None
    texts: Optional[List[TextDetectionResult]] = None
    safety_scores: Optional[SafeSearchResult] = None
