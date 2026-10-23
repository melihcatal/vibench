import dataclasses
from typing import Optional


@dataclasses.dataclass
class SynthesisRequest:
    text: str
    voice_name: Optional[str] = None
    language_code: str = "en-US"
    audio_encoding: str = "MP3"  # LINEAR16, MP3, OGG_OPUS


@dataclasses.dataclass
class SSMLSynthesisRequest:
    ssml: str
    voice_name: Optional[str] = None
    language_code: str = "en-US"
    audio_encoding: str = "MP3"


@dataclasses.dataclass
class Voice:
    name: str
    language_codes: list[str]
    gender: str
    natural_sample_rate_hertz: int


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class ContentSafetyRequest:
    text: str


@dataclasses.dataclass
class EmbeddingRequest:
    text: str


@dataclasses.dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: str = "en-US"
