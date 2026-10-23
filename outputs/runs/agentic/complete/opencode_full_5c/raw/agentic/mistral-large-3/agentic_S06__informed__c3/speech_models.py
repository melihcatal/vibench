from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum


class AudioEncoding(str, Enum):
    """Supported audio encoding formats."""

    MP3 = "MP3"
    LINEAR16 = "LINEAR16"
    OGG_OPUS = "OGG_OPUS"
    MULAW = "MULAW"
    ALAW = "ALAW"


class SsmlVoiceGender(str, Enum):
    """Supported SSML voice genders."""

    MALE = "MALE"
    FEMALE = "FEMALE"
    NEUTRAL = "NEUTRAL"


@dataclass
class Voice:
    """Represents a voice for synthesis."""

    name: str
    language_codes: List[str]
    ssml_gender: SsmlVoiceGender


@dataclass
class SynthesisRequest:
    """Represents a synthesis request."""

    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_name: str = "en-US-Wavenet-D"
    language_code: str = "en-US"
    audio_encoding: AudioEncoding = AudioEncoding.MP3


@dataclass
class SynthesisResponse:
    """Represents a synthesis response."""

    audio_content: bytes
