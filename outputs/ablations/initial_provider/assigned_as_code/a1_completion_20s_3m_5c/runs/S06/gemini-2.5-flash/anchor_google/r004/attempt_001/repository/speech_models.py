from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    audio_encoding: str = "MP3"
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    volume_gain_db: Optional[float] = None

@dataclass
class SynthesisResponse:
    audio_bytes: bytes
    content_type: str

@dataclass
class Voice:
    name: str
    language_codes: list[str]
    ssml_gender: str
    natural_sample_rate_hertz: int

@dataclass
class VoiceListResponse:
    voices: list[Voice]
