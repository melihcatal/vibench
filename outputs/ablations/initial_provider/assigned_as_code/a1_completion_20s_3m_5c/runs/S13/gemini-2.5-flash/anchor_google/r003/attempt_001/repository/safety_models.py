from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ModerationRequest:
    text: str
    language_code: str = "en"

@dataclass
class ModerationResponse:
    # This will be a simplified representation.
    # The actual Content Safety API response is more complex.
    categories: Dict[str, float]  # e.g., {"violence": 0.9, "sexual": 0.1}
    is_safe: bool
    raw_response: Dict[str, Any] = None

@dataclass
class RedactionRequest:
    text: str
    language_code: str = "en"
    harm_types: Optional[List[str]] = None

@dataclass
class RedactionResponse:
    redacted_text: str
    raw_response: Dict[str, Any] = None

@dataclass
class SummaryRequest:
    decisions: List[Dict[str, Any]] # List of moderation decisions

@dataclass
class SummaryResponse:
    summary: str

@dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclass
class TranslationResponse:
    translated_text: str

@dataclass
class EmbeddingRequest:
    text: str

@dataclass
class EmbeddingResponse:
    embedding: List[float]

@dataclass
class AudioBriefRequest:
    text: str
    language_code: str = "en-US"
    voice_name: str = "en-US-Standard-C" # Example voice

@dataclass
class AudioBriefResponse:
    audio_content: bytes
