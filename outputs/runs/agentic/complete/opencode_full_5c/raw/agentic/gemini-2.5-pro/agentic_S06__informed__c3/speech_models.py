from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Voice:
    name: str
    language_code: str
    ssml_gender: str


@dataclass
class SynthesisInput:
    text: Optional[str] = None
    ssml: Optional[str] = None


@dataclass
class VoiceSelectionParams:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None


@dataclass
class AudioConfig:
    audio_encoding: str
