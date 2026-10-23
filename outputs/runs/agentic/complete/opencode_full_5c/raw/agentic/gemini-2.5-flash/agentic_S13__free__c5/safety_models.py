import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class ModerationRequest:
    text: str


@dataclasses.dataclass
class ModerationCategory:
    name: str
    score: float


@dataclasses.dataclass
class ModerationResponse:
    is_unsafe: bool
    categories: List[ModerationCategory]
    provider: str = "Google Cloud Natural Language API"


@dataclasses.dataclass
class BatchModerationRequest:
    texts: List[str]


@dataclasses.dataclass
class BatchModerationResponse:
    decisions: List[ModerationResponse]
    provider: str = "Google Cloud Natural Language API"


@dataclasses.dataclass
class RedactionRequest:
    text: str


@dataclasses.dataclass
class RedactionSpan:
    text_content: str
    start_offset: int
    end_offset: int
    replacement_char_count: int


@dataclasses.dataclass
class RedactionResponse:
    redacted_text: str
    redaction_spans: List[RedactionSpan]
    provider: str = "Google Cloud Natural Language API"


@dataclasses.dataclass
class TextSafetyDecision:
    text: str
    allowed: bool
    reasons: List[str]
    threshold_provider: str = (
        "Local Thresholding Logic"  # Explicitly not an external provider
    )


@dataclasses.dataclass
class SummaryRequest:
    text: str
    max_tokens: int = 100


@dataclasses.dataclass
class SummaryResponse:
    summary_text: str
    provider: str = "OpenAI"


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str
    detected_language: Optional[str] = None
    provider: str = "Google Cloud Translation API"


@dataclasses.dataclass
class EmbeddingRequest:
    text: str


@dataclasses.dataclass
class EmbeddingResponse:
    embedding: List[float]
    provider: str = "OpenAI"


@dataclasses.dataclass
class AudioBriefRequest:
    text: str
    language_code: str = "en-US"
    voice_name: str = "en-US-Wavenet-D"


@dataclasses.dataclass
class AudioBriefResponse:
    audio_content: bytes
    provider: str = "Google Cloud Text-to-Speech API"
