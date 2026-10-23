from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_name: str = "en-US-JennyNeural"
    locale: str = "en-US"


@dataclass
class SynthesisResponse:
    audio_chunk: bytes