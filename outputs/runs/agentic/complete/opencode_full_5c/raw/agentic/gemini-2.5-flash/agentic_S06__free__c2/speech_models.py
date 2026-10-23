from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_name: Optional[str] = None
    language_code: str = "en-US"
    gender: Literal["MALE", "FEMALE", "NEUTRAL", "UNSPECIFIED"] = "UNSPECIFIED"
    audio_encoding: Literal["LINEAR16", "MP3", "OGG_OPUS"] = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0


@dataclass
class VoiceSelectionParams:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[Literal["MALE", "FEMALE", "NEUTRAL", "UNSPECIFIED"]] = None


@dataclass
class AudioConfigParams:
    audio_encoding: Literal["LINEAR16", "MP3", "OGG_OPUS"]
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None


@dataclass
class SynthesisResponse:
    audio_content: bytes
