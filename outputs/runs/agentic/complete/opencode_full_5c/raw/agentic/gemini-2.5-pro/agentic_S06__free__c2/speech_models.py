from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Voice:
    name: str
    language_code: str
    ssml_gender: str


@dataclass
class SynthesisRequest:
    text: str
    voice: Optional[Voice] = None
    language_code: str = "en-US"


@dataclass
class SsmlSynthesisRequest:
    ssml: str
    voice: Optional[Voice] = None
    language_code: str = "en-US"


@dataclass
class AudioResponse:
    audio_content: bytes


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class SafetyCheckRequest:
    text: str


@dataclass
class EmbeddingRequest:
    texts: List[str]


@dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: str = "en-US"
