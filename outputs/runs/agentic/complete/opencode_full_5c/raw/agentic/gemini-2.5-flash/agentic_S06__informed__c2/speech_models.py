import dataclasses
from typing import Optional


@dataclasses.dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_name: Optional[str] = None
    language_code: str = "en-US"
    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0


@dataclasses.dataclass
class VoiceSelection:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None


@dataclasses.dataclass
class ContentSafetyRequest:
    text_content: str


@dataclasses.dataclass
class EmbeddingRequest:
    text: str


@dataclasses.dataclass
class TranscriptionRequest:
    audio_content: bytes
    language_code: str = "en-US"
    sample_rate_hertz: Optional[int] = None
