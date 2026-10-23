import dataclasses
from typing import Optional, Literal


@dataclasses.dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None


@dataclasses.dataclass
class VoiceSelectionParams:
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
    voice: VoiceSelectionParams
    audio_config: AudioConfig


@dataclasses.dataclass
class SynthesizeSpeechResponse:
    audio_content: bytes


@dataclasses.dataclass
class TranslateTextRequest:
    text: str
    target_language_code: str
    parent: str


@dataclasses.dataclass
class TranslateTextResponse:
    translated_text: str


@dataclasses.dataclass
class AnalyzeTextRequest:
    text: str
    do_not_store: bool = True
    comment_analyzer_key: str = ""


@dataclasses.dataclass
class AnalyzeTextResponse:
    attribute_scores: dict


@dataclasses.dataclass
class EmbedContentRequest:
    text: str


@dataclasses.dataclass
class EmbedContentResponse:
    embedding: list[float]


@dataclasses.dataclass
class TranscribeAudioRequest:
    audio_content: bytes
    language_code: str
    sample_rate_hertz: Optional[int] = None
