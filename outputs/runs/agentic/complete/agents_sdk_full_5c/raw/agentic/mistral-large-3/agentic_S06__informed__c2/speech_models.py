from typing import Iterator, Optional
from dataclasses import dataclass, field
from enum import Enum


class AudioFormat(str, Enum):
    WAV = "audio/wav"
    MP3 = "audio/mp3"
    OGG = "audio/ogg"


@dataclass
class Voice:
    name: str
    language: str
    gender: str
    description: str = ""
    customizable: bool = False
    url: Optional[str] = None


@dataclass
class SynthesisRequest:
    text: str
    voice: Optional[str] = None
    audio_format: AudioFormat = AudioFormat.WAV
    ssml_enabled: bool = False


@dataclass
class SynthesisResponse:
    audio: bytes
    
    def audio_chunks(self, chunk_size: int = 4096) -> Iterator[bytes]:
        for i in range(0, len(self.audio), chunk_size):
            yield self.audio[i:i + chunk_size]