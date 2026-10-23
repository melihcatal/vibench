import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class TextModerationRequest:
    text: str

@dataclasses.dataclass
class TextModerationResponse:
    toxicity_score: float
    categories: Optional[dict] = None # For future expansion with more detailed category scores

@dataclasses.dataclass
class BatchModerationRequest:
    texts: List[str]

@dataclasses.dataclass
class BatchModerationResponse:
    results: List[TextModerationResponse]

@dataclasses.dataclass
class RedactionRequest:
    text: str
    threshold: float = 0.8 # Default threshold for redaction

@dataclasses.dataclass
class RedactionResponse:
    original_text: str
    redacted_text: str
    redacted_spans: List[dict] # List of {"start": int, "end": int, "replacement": str}

@dataclasses.dataclass
class ModerationDecision:
    text: str
    toxicity_score: float
    decision: str # "allow", "flag", "block"
    reason: Optional[str] = None

@dataclasses.dataclass
class AppealTranslateRequest:
    text: str
    target_language: str = "en"

@dataclasses.dataclass
class AppealTranslateResponse:
    original_text: str
    translated_text: str
    detected_language: Optional[str] = None

@dataclasses.dataclass
class EmbedRequest:
    text: str

@dataclasses.dataclass
class EmbedResponse:
    embedding: List[float]

@dataclasses.dataclass
class AudioBriefRequest:
    text: str
    voice_name: str = "en-US-Wavenet-D" # Example voice

@dataclasses.dataclass
class AudioBriefResponse:
    audio_content: bytes
