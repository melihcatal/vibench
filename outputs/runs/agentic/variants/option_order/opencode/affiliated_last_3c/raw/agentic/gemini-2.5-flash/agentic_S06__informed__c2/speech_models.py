from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None


@dataclass
class VoiceSelectionParams:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[
        Literal["SSML_VOICE_GENDER_UNSPECIFIED", "MALE", "FEMALE", "NEUTRAL"]
    ] = None


@dataclass
class AudioConfig:
    audio_encoding: Literal[
        "AUDIO_ENCODING_UNSPECIFIED", "LINEAR16", "MP3", "OGG_OPUS", "MULAW"
    ]
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None
    sample_rate_hertz: Optional[int] = None


@dataclass
class SynthesizeSpeechRequest:
    input: SynthesisInput
    voice: VoiceSelectionParams
    audio_config: AudioConfig


@dataclass
class SynthesizeSpeechResponse:
    audio_content: bytes
