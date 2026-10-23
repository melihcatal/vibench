from dataclasses import dataclass
from typing import List, Optional


@dataclass
class VoiceParams:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None


@dataclass
class AudioConfig:
    audio_encoding: str
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None
    sample_rate_hertz: Optional[int] = None


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice: VoiceParams
    audio_config: AudioConfig


@dataclass
class SynthesisResponse:
    audio_content: bytes
