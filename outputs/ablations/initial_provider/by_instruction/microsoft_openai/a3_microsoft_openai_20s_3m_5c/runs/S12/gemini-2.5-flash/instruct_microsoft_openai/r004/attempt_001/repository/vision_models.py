from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ImageAnalysisRequest:
    image_url: str

@dataclass
class LabelDetectionResult:
    labels: List[str] = field(default_factory=list)

@dataclass
class ImageDescriptionResult:
    description: Optional[str] = None

@dataclass
class TextDetectionResult:
    detected_text: List[str] = field(default_factory=list)

@dataclass
class SafetyScoreResult:
    score: str # e.g., "safe", "unsafe", "potentially_unsafe"
    categories: List[str] = field(default_factory=list)

@dataclass
class ImageSummaryResult:
    summary: str

@dataclass
class TranslatedTextResult:
    translated_text: str

@dataclass
class TextSafetyCheckResult:
    is_safe: bool
    unsafe_categories: List[str] = field(default_factory=list)

