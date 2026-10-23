from dataclasses import dataclass
from typing import List, Optional
import re


@dataclass
class TextToSpeechRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class SsmlRequest:
    ssml: str
    voice: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class AudioResponse:
    audio_bytes: bytes
    content_type: str = 'audio/mpeg'


@dataclass
class VoiceSelectionRequest:
    locale: Optional[str] = None
    gender: Optional[str] = None
    name: Optional[str] = None


@dataclass
class VoiceInfo:
    name: str
    locale: str
    gender: str
    provider: str


@dataclass
class VoiceListResponse:
    voices: List[VoiceInfo]

    def pick_best(self) -> VoiceInfo:
        if not self.voices:
            raise ValueError('No voices available')
        return self.voices[0]


def normalize_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def normalize_ssml(ssml: str) -> str:
    return re.sub(r'\s+', ' ', ssml).strip()
