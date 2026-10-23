from dataclasses import dataclass
from typing import Optional, Literal

class AudioFormat(Literal["mp3", "wav", "ogg"]):
    pass
@dataclass
class SynthesisInput:
    text: str
@dataclass
class SSMLSynthesisInput:
    ssml: str
@dataclass
class VoiceInfo:
    name: str
    locale: str
    gender: str
    style: Optional[str] = None