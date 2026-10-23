from dataclasses import dataclass
from typing import Optional, List


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str = "en-US"
    voice_name: Optional[str] = None


@dataclass
class Voice:
    name: str
    language_codes: List[str]
    ssml_gender: str


@dataclass
class SynthesizedSpeech:
    audio_content: bytes
