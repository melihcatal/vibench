from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Label:
    name: str
    confidence: float
    topicality: Optional[float] = None

@dataclass
class LabelDetectionResult:
    labels: List[Label]

@dataclass
class DetectedText:
    text: str
    confidence: float
    bounding_box: Dict[str, float]

@dataclass
class TextDetectionResult:
    texts: List[DetectedText]

@dataclass
class ImageDescriptionResult:
    description: str

@dataclass
class SafetyCategory:
    name: str
    severity: int

@dataclass
class ImageSafetyResult:
    categories: List[SafetyCategory]

@dataclass
class VisualAnalysisSummary:
    labels: List[Label]
    texts: List[DetectedText]
    description: str
    safety_categories: List[SafetyCategory]

@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class TextSafetyResult:
    is_safe: bool
    unsafe_categories: List[str]
    confidence: Optional[float] = None

@dataclass
class ArchiveResult:
    object_key: str
    archive_url: str