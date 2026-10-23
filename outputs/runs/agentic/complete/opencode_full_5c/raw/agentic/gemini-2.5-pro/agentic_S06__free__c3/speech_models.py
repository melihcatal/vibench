from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Voice:
    language_code: str
    name: str
    ssml_gender: str
    natural_sample_rate_hertz: int


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None


@dataclass
class SynthesisResponse:
    audio_content: bytes


@dataclass
class TranslationRequest:
    script_content: str
    target_language: str
    source_language: str = "en-US"


@dataclass
class SafetyCheckRequest:
    script_content: str


@dataclass
class EmbeddingRequest:
    script_content: str


@dataclass
class TranscriptionRequest:
    audio_content: bytes
