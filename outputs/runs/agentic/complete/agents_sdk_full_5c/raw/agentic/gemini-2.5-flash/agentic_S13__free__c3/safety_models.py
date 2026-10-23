from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class Score:
    value: float
    type: str = "PROBABILITY" # As typically seen in Perspective API

@dataclass
class SummaryScore:
    value: float

@dataclass
class AttributeScore:
    summaryScore: SummaryScore
    spanScores: Optional[List[Dict]] = field(default_factory=list) # Detailed scores for spans

@dataclass
class ModerationResult:
    """
    Represents the structure of a moderation result, primarily from Perspective API.
    """
    attributeScores: Dict[str, AttributeScore]
    languages: Optional[List[str]] = field(default_factory=list)
    detectedLanguages: Optional[List[str]] = field(default_factory=list)

@dataclass
class BatchModerationRequest:
    """
    Represents a request for batch moderation.
    """
    texts: List[str]

@dataclass
class RedactionFinding:
    """
    Represents a finding from the DLP API for redaction/inspection.
    """
    quote: str
    info_type: str
    likelihood: str
    start_index: int
    end_index: int

@dataclass
class RedactionResult:
    """
    Represents the result of a redaction operation.
    """
    original_text: str
    redacted_text: Optional[str] = None
    findings: List[RedactionFinding] = field(default_factory=list)

@dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclass
class TranslationResult:
    translated_text: str
    detected_language_code: Optional[str] = None

@dataclass
class EmbeddingRequest:
    text: str

@dataclass
class EmbeddingResult:
    embedding: List[float]

@dataclass
class AudioBriefRequest:
    text: str
    language_code: str = "en-US"
    voice_name: str = "en-US-Wavenet-D" # Example voice
    speaking_rate: float = 1.0
    pitch: float = 0.0

@dataclass
class AudioBriefResult:
    audio_content: bytes # Raw audio bytes
