from dataclasses import dataclass, field
from typing import Literal, Optional

@dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None

@dataclass
class VoiceSelectionParams:
    language_code: str = "en-US"
    name: Optional[str] = None
    ssml_gender: Optional[Literal["MALE", "FEMALE", "NEUTRAL"]] = None

@dataclass
class AudioConfig:
    audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS"] = "MP3"
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

@dataclass
class Voice:
    name: str
    supported_language_codes: list[str]
    ssml_gender: Literal["MALE", "FEMALE", "NEUTRAL", "UNSPECIFIED"]
    natural_sample_rate_hertz: int

@dataclass
class ListVoicesResponse:
    voices: list[Voice] = field(default_factory=list)
