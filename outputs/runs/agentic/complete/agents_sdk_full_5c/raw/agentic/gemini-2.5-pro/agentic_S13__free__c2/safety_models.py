from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class ModerationRequest:
    text: str

@dataclass
class ModerationResponse:
    is_safe: bool
    scores: Dict[str, float]
    raw_response: Any

@dataclass
class BatchModerationResponse:
    results: List[ModerationResponse]

@dataclass
class RedactionRequest:
    text: str

@dataclass
class RedactionResponse:
    original_text: str
    redacted_text: str
    redacted_spans: List[Dict[str, Any]]

@dataclass
class TranslationRequest:
    text: str
    target_language: str = "EN-US"

@dataclass
class TranslationResponse:
    original_text: str
    translated_text: str
    detected_source_language: Optional[str] = None
