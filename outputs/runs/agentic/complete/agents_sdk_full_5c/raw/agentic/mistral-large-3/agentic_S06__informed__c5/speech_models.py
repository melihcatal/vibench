from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SynthesisRequest:
    text: str
    voice_id: Optional[str] = None
    ssml: bool = False

@dataclass
class SynthesisResponse:
    audio_bytes: bytes
    mime_type: str

@dataclass
class VoiceInfo:
    voice_id: str
    name: str
    category: str
    languages: List[str]