from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class ImagePayload:
    image_bytes: bytes

@dataclass
class LabelAnnotation:
    description: str
    score: float

@dataclass
class DetectedLabels:
    labels: List[LabelAnnotation] = field(default_factory=list)

@dataclass
class TextAnnotation:
    text: str
    bounds: List[Dict[str, Any]] # Vertices for bounding box

@dataclass
class DetectedText:
    texts: List[TextAnnotation] = field(default_factory=list)

@dataclass
class SafeSearchAnnotation:
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str

@dataclass
class ImageModerationResult:
    safe_search_annotation: Optional[SafeSearchAnnotation] = None

@dataclass
class ImageDescription:
    description: str
    confidence: float
