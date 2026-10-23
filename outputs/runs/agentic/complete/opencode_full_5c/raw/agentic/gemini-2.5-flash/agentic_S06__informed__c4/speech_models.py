import dataclasses
from typing import Optional, List, Dict, Any


@dataclasses.dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None


@dataclasses.dataclass
class VoiceSelectionParams:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None  # e.g., 'MALE', 'FEMALE', 'NEUTRAL'


@dataclasses.dataclass
class AudioConfig:
    audio_encoding: str  # e.g., 'LINEAR16', 'MP3'
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None
    sample_rate_hertz: Optional[int] = None


@dataclasses.dataclass
class SynthesizeSpeechRequest:
    input: SynthesisInput
    voice: VoiceSelectionParams
    audio_config: AudioConfig


@dataclasses.dataclass
class SynthesizeSpeechResponse:
    audio_content: bytes


@dataclasses.dataclass
class Voice:
    name: str
    language_codes: List[str]
    ssml_gender: str
    natural_sample_rate_hertz: int


@dataclasses.dataclass
class ListVoicesResponse:
    voices: List[Voice]
