from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ModerationRequest:
    text: str

@dataclass
class TextAnalysisResult:
    text: str
    categories: Dict[str, float] # e.g., {'Hate': 0.1, 'SelfHarm': 0.05}
    is_unsafe: bool # Basic flag if any category score > 0 before thresholding

@dataclass
class ModerationDecision:
    original_text: str
    decision: str # e.g., 'Allowed', 'Flagged'
    reasons: List[str]
    scores: Dict[str, float]

@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    detected_info_types: List[str]

@dataclass
class ModerationSummary:
    original_texts: List[str]
    decisions: List[ModerationDecision]
    summary_text: str

@dataclass
class TranslatedText:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class TextEmbedding:
    text: str
    embedding: List[float]

@dataclass
class AudioBrief:
    text_brief: str
    audio_content: bytes
    audio_format: str
