from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SynthesizeTextRequest:
    text: str
    voice_name: str
    language_code: str = "en-US"
    audio_encoding: str = "MP3"


@dataclass
class SynthesizeSsmlRequest:
    ssml: str
    voice_name: str
    language_code: str = "en-US"
    audio_encoding: str = "MP3"
    pitch: float = 0.0
    speaking_rate: float = 1.0


@dataclass
class Voice:
    name: str
    language_codes: List[str]
    gender: str  # e.g., "MALE", "FEMALE", "NEUTRAL"


@dataclass
class VoiceSelectionResponse:
    voices: List[Voice]
