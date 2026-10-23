from dataclasses import dataclass
from typing import Optional, List, Union
from enum import Enum


class AudioEncoding(Enum):
    MP3 = "MP3"
    LINEAR16 = "LINEAR16"
    OGG_OPUS = "OGG_OPUS"


@dataclass
class VoiceSelection:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None


@dataclass
class AudioConfig:
    audio_encoding: AudioEncoding = AudioEncoding.MP3
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None
    sample_rate_hertz: Optional[int] = None


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice: Optional[VoiceSelection] = None
    audio_config: Optional[AudioConfig] = None


@dataclass
class SynthesisResponse:
    audio_content: bytes
    audio_encoding: AudioEncoding
