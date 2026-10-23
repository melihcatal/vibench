from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TextCategory:
    category: str
    severity: int  # e.g., 0-7 from Azure Content Safety

@dataclass
class ModerationResult:
    text: str
    categories: List[TextCategory]

@dataclass
class BatchModerationInput:
    texts: List[str]

@dataclass
class BatchModerationOutput:
    results: List[ModerationResult]

@dataclass
class DlpDetection:
    info_type: str
    quote: str
    start: int
    end: int

@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    detections: List[DlpDetection] # Details about what was detected (if available from inspect_content)

@dataclass
class ThresholdDecision:
    text: str
    decision: str  # e.g., "ALLOW", "FLAG"
    flagged_categories: List[TextCategory]

@dataclass
class SummarizationInput:
    decision_text: str
    flagged_categories: List[str] # e.g., ['Hate', 'Violence']

@dataclass
class SummarizationOutput:
    summary: str

@dataclass
class TranslationInput:
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class TranslationOutput:
    translated_text: str
    detected_source_language: Optional[str] = None

@dataclass
class EmbeddingInput:
    text: str

@dataclass
class EmbeddingOutput:
    embedding: List[float]

@dataclass
class AudioBriefInput:
    text: str

@dataclass
class AudioBriefOutput:
    audio_content: bytes
