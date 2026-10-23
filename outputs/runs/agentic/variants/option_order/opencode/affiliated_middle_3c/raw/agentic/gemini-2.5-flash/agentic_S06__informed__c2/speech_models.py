import dataclasses
from typing import Literal, Optional


@dataclasses.dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None


@dataclasses.dataclass
class VoiceSelection:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[Literal["MALE", "FEMALE", "NEUTRAL"]] = None


@dataclasses.dataclass
class AudioConfig:
    audio_encoding: Literal["LINEAR16", "MP3", "OGG_OPUS"]
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None


@dataclasses.dataclass
class SynthesizeSpeechRequest:
    input: SynthesisInput
    voice: VoiceSelection
    audio_config: AudioConfig


@dataclasses.dataclass
class SynthesizeSpeechResponse:
    audio_content: bytes


@dataclasses.dataclass
class Voice:
    name: str
    language_codes: list[str]
    ssml_gender: Literal["MALE", "FEMALE", "NEUTRAL"]
    natural_sample_rate_hertz: int


@dataclasses.dataclass
class TranslateTextRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None


@dataclasses.dataclass
class TranslateTextResponse:
    translated_text: str


@dataclasses.dataclass
class ContentSafetyRequest:
    text: str


@dataclasses.dataclass
class ContentSafetyResponse:
    is_safe: bool
    reasons: list[str]


@dataclasses.dataclass
class EmbeddingRequest:
    text: str


@dataclasses.dataclass
class EmbeddingResponse:
    embedding: list[float]


@dataclasses.dataclass
class TranscriptionRequest:
    audio_content: bytes
    language_code: str
    sample_rate_hertz: int


@dataclasses.dataclass
class TranscriptionResponse:
    transcript: str
