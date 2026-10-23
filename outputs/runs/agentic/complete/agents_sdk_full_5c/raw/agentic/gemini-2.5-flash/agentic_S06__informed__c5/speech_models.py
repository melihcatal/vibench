from dataclasses import dataclass
from typing import Optional

@dataclass
class SynthesisRequest:
    text: str
    voice_id: str = "Joanna"
    output_format: str = "mp3"
    text_type: str = "text"

@dataclass
class SynthesisResponse:
    audio_bytes: bytes
    content_type: str

@dataclass
class VoiceInfo:
    voice_id: str
    language_code: str
    gender: str
    name: str
    supported_audio_formats: list
