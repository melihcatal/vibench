from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class ImageInput:
    image_uri: str
    image_bytes: bytes = None

@dataclass
class LabelDetectionResult:
    labels: List[str]

@dataclass
class ImageDescriptionResult:
    description: str

@dataclass
class TextDetectionResult:
    full_text: str
    individual_texts: List[str] = field(default_factory=list)

@dataclass
class SafetyDetectionResult:
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str

@dataclass
class VisualAnalysisResult:
    image_uri: str
    labels: List[str] = field(default_factory=list)
    description: str = ""
    detected_text: str = ""
    safety_scores: Dict[str, str] = field(default_factory=dict)
