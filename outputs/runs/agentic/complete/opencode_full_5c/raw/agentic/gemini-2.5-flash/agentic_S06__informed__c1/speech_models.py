from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class VoiceSelection:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[Literal["MALE", "FEMALE", "NEUTRAL"]] = None


@dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None


@dataclass
class AudioConfig:
    audio_encoding: Literal["LINEAR16", "MP3", "OGG_OPUS"] = "MP3"
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None
