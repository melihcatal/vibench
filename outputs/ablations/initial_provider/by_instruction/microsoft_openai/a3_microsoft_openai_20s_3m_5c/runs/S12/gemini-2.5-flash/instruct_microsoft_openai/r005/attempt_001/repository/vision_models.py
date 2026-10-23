from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class ImageInput:
    image_url: Optional[str] = None
    image_base64: Optional[str] = None

@dataclass
class Label:
    name: str
    confidence: float

@dataclass
class ImageLabelsResponse:
    labels: List[Label] = field(default_factory=list)

@dataclass
class ImageDescriptionResponse:
    description: str

@dataclass
class DetectedText:
    text: str
    bounding_boxes: List[List[int]] = field(default_factory=list) # [x1, y1, x2, y2, ...]

@dataclass
class ImageTextDetectionResponse:
    texts: List[DetectedText] = field(default_factory=list)

@dataclass
class SafetyAnnotation:
    category: str
    likelihood: str # e.g., 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'

@dataclass
class ImageSafetyResponse:
    annotations: List[SafetyAnnotation] = field(default_factory=list)

# New models for Later-Step files

@dataclass
class ImageAnalysisSummary:
    summary_text: str

@dataclass
class TranslatedText:
    translated_description: str
    source_language: str
    target_language: str

@dataclass
class TextSafetyAnnotation:
    category: str
    score: float # e.g., 0.0 to 1.0 for different categories like "sexual", "hate", etc.
    is_safe: bool

@dataclass
class VisualSafetyTextResponse:
    annotations: List[TextSafetyAnnotation] = field(default_factory=list)

@dataclass
class ArchiveResult:
    archive_url: str
    file_name: str