from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    audio_encoding: str = "MP3" # Corresponds to google.cloud.texttospeech.AudioEncoding

@dataclass
class SynthesisResponse:
    audio_bytes: bytes
    content_type: str

@dataclass
class Voice:
    name: str
    language_codes: list[str]
    gender: str
    natural_sample_rate_hertz: int

@dataclass
class VoiceSelection:
    language_code: str
    name: Optional[str] = None
    gender: Optional[str] = None
