from typing import Literal, Dict, Any
from dataclasses import dataclass

@dataclass
class SynthesisRequest:
    text: str
    voice_id: str
    output_format: Literal["mp3", "pcm", "ogg_vorbis"] = "mp3"

@dataclass
class SynthesisResponse:
    audio_content: bytes
    content_type: str

@dataclass
class VoiceInfo:
    voice_id: str
    name: str
    gender: str
    language_code: str
    supported_audio_formats: list[str]
