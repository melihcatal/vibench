from dataclasses import dataclass
from typing import List, Optional


@dataclass
classSpeechSynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str = "en-US"
    voice_name: Optional[str] = None


@dataclass
classVoice:
    name: str
    language_codes: List[str]


@dataclass
classSpeechSynthesisResponse:
    audio_content: bytes


@dataclass
classTranslationRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None


@dataclass
classTranslationResponse:
    translated_text: str


@dataclass
classContentSafetyRequest:
    text: str


@dataclass
classContentSafetyResponse:
    is_safe: bool
    categories: Optional[dict] = None


@dataclass
classEmbeddingRequest:
    text: str


@dataclass
classEmbeddingResponse:
    embedding: List[float]


@dataclass
classTranscriptionRequest:
    audio_content: bytes
    language_code: str = "en-US"


@dataclass
classTranscriptionResponse:
    transcript: str
    confidence: float

